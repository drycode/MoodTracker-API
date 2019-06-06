from datetime import datetime
from collections import OrderedDict

from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(258))
    current_streak = db.Column(db.Integer, default=0)
    best_streak = db.Column(db.Integer, default=0)
    moods = db.relationship("MoodEntry", backref="author", lazy="dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        print(type(self.password_hash))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_password(self):
        return self.password

    def update_current_streak(self):
        pass

    def asdict(self):
        return OrderedDict(
            id=self.id,
            username=self.username,
            email=self.email,
            current_streak=self.current_streak,
            best_streak=self.best_streak,
        )

    def __repr__(self):
        return "<User {}>".format(self.username)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class MoodEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    mood_score = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<MoodEntry Score:{} Time:{}>".format(self.mood_score, self.timestamp)

    def _verify_mood_range(self, mood):
        if not isinstance(mood, int):
            return False
        if 0 > mood > 10:
            return False
        else:
            return True
