"""This module contains all routing information for the Flask server."""
from scipy.stats import percentileofscore
from flask import jsonify, redirect, request
from flask_login import current_user, login_user, login_required, logout_user

from app import app, db
from app.models import User, MoodEntry, _verify_mood_range
from sqlalchemy import func


@app.route("/health")
def check_server():
    """Checks if the server is active."""
    return jsonify({"msg": "Flask is up and running!"})


@app.route("/login", methods=["GET", "POST"])
def login():
    """Allows users to login"""
    if current_user.is_authenticated:
        return redirect("/mood")

    username, email, password = _create_user_helper(request)

    user = User.query.filter_by(username=username).first()

    if user is None:
        user = User(username=str(username), email=str(email))
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        login_user(user, remember=True)
        return jsonify(
            {
                "msg": f"Successfully created user with username {user.username}",
                "User": user.asdict(),
            }
        )

    login_user(user, remember=True)
    if not user.check_password(password):
        return jsonify("not a valid user")

    return redirect("/login")


@app.route("/getuser")
def getuser():
    """Returns active user"""
    user_id = current_user.get_id()
    if user_id:
        return jsonify(
            {
                "msg": "{} is active.".format(User.query.filter_by(id=user_id).first()),
                "user_id": f"{user_id}",
            }
        )
    return jsonify({"msg": "There is no current user. Please log in."})


@app.route("/logout")
def logout():
    """Allows users to logout"""
    logout_user()
    return jsonify({"msg": "You have been logged out."})


@app.route("/mood", methods=["POST"])
def post_mood():
    """Posts a mood value to a persisted datastore"""
    if request.json:
        req = request.json
        mood_score = _verify_mood_range(req.get("mood_score", None))

    else:
        req = request.args
        mood_score = _verify_mood_range(req.get("mood_score", type=int))

    if not req:
        return jsonify({"msg": "Must provide valid parameters."})

    if not current_user:
        return redirect("/login")

    current_user.update_streaks(method_type="POST")
    entry = MoodEntry(user_id=current_user.get_id(), mood_score=mood_score)
    db.session.add(entry)
    db.session.commit()
    return jsonify(entry.asdict())


@login_required
@app.route("/mood", methods=["GET"])
def get_moods():
    """Gets all mood values for a particular user"""
    if not current_user:
        return redirect("/login")

    current_user.update_streaks(method_type="GET")
    db.session.commit()

    response = {
        "mood_entries": [
            entry.asdict()
            for entry in db.session.query(MoodEntry)
            .filter(current_user.get_id() == MoodEntry.user_id)
            .all()
        ],
        "current_streak": current_user.get_current_streak(),
        "best_streak": current_user.get_best_streak(),
    }

    percentile = _calculate_streak_percentile()
    if percentile >= 50:
        response.update({"percentile": percentile})

    return jsonify(response)


def _create_user_helper(req):
    if req.json:
        username = req.json["username"]
        email = req.json["email"]
        password = req.json["password"]

    else:
        username = req.args.get("username", type=str)
        email = req.args.get("email", type=str)
        password = req.args.get("password", type=str)

    return username, email, password


def _calculate_streak_percentile():
    scores_arr = [
        user.best_streak
        for user in db.session.query(User).order_by(User.best_streak).all()
    ]

    return percentileofscore(scores_arr, current_user.get_best_streak())
