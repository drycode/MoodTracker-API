"""This module stores all db models for the flask application."""

from datetime import datetime
from collections import OrderedDict

from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


STR_DATE_FRMT = "%b %d %Y %H:%M:%S"


class User(UserMixin, db.Model):
    """The User model represents client side users who wish to access the
    API.
    Passwords will be stored using an SHA256 hash.
    Streaks are incremented for consecutive days posting MoodEntries to the
    Application"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(258))
    current_streak = db.Column(db.Integer, default=0)
    best_streak = db.Column(db.Integer, default=0)
    moods = db.relationship("MoodEntry", backref="author", lazy="dynamic")

    def set_password(self, password):
        """Converts user provided password to a SHA256 hashed password."""
        self.password_hash = generate_password_hash(password)
        print(type(self.password_hash))

    def check_password(self, password):
        """Verifies that user provided password matches hashed password."""
        return check_password_hash(self.password_hash, password)

    def update_current_streak(self):
        """Updates current streak for a user using timestamps from mood entries."""

    def asdict(self):
        """Returns instance of dict to represent User object."""
        return OrderedDict(
            id=self.id,
            username=self.username,
            email=self.email,
            current_streak=self.current_streak,
            best_streak=self.best_streak,
        )

    def __repr__(self):
        """Returns instance of string to represent User object."""
        return "<User {}>".format(self.username)


@login.user_loader
def load_user(id):
    """Saves session data about current_user flask-login."""
    return User.query.get(int(id))


class MoodEntry(db.Model):
    """The Mood Entry model represents instances where the client side user
    documents a mood score value."""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    mood_score = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())

    def asdict(self):
        return OrderedDict(
            id=self.id,
            user_id=self.user_id,
            mood_score=self.mood_score,
            timestamp=(self.timestamp.strftime(STR_DATE_FRMT)),
        )

    def get_timestamp(self):
        """Returns unix timestamp for mood entry"""
        return self.timestamp

    def __repr__(self):
        return "<MoodEntry Score:{} Time:{}>".format(self.mood_score, self.timestamp)


def _verify_mood_range(mood):
    if not isinstance(mood, int):
        raise TypeError
    if 0 > mood or mood > 10:
        raise ValueError
    else:
        return mood
