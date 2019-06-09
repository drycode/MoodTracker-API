"""This module contains all routing information for the Flask server."""
from flask import jsonify, redirect, request, abort
from flask_login import current_user, login_user, login_required, logout_user
from webargs.flaskparser import parser

from app import app, db, errors
from app.helpers import calculate_streak_percentile
from app.models import User, MoodEntry
from app.query_param_validators import user_args, mood_args


@app.route("/health")
def check_server():
    """Checks if the server is active."""
    return jsonify({"msg": "Flask is up and running!"})


@app.route("/login", methods=["POST", "GET"])
def login():
    """Allows users to login"""

    args = parser.parse(user_args, request)

    user = User.query.filter_by(username=args["username"]).first()

    if user is None:
        user = User(username=str(args["username"]), email=str(args["email"]))
        user.set_password(args["password"])
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
    if not current_user.check_password(args["password"]):
        return jsonify("The password you entered was invalid.")

    if current_user.is_authenticated:
        return redirect("/mood")

    print("NO CONDITIONS WERE MET!")


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
    if not current_user.is_authenticated:
        return redirect("/login")
    logout_user()
    return jsonify({"msg": "You have been logged out."})


@app.route("/mood", methods=["POST"])
@login_required
def post_mood():
    """Posts a mood value to a persisted datastore"""
    args = parser.parse(mood_args, request)

    mood_score = int(args["mood_score"])

    current_user.update_streaks(method_type="POST")
    entry = MoodEntry(user_id=current_user.get_id(), mood_score=mood_score)
    db.session.add(entry)
    db.session.commit()
    return jsonify(entry.asdict())


@app.route("/mood", methods=["GET"])
@login_required
def get_moods():
    """Gets all mood values for a particular user"""
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

    percentile = calculate_streak_percentile()
    if percentile >= 50:
        response.update({"percentile": percentile})

    return jsonify(response)

