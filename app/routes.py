"""This module contains all routing information for the Flask server."""

from flask import jsonify, redirect, request
from flask_login import current_user, login_user, login_required, logout_user

from app import app, db
from app.models import User


@app.route("/health")
def check_server():
    """Checks if the server is active."""
    return jsonify({"msg": "Flask is up and running!"})


@app.route("/login", methods=["GET", "POST"])
def login():
    """Allows users to login"""
    if current_user.is_authenticated:
        return redirect("/mood")

    req = request.json
    user = User.query.filter_by(username=req["username"]).first()

    if user is None:
        user = User(username=str(req["username"]), email=str(req["email"]))
        user.set_password(req["password"])
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
    if not user.check_password(req["password"]):
        return jsonify("not a valid user")

    return redirect("/login")


@app.route("/getuser")
def getuser():
    """Returns active user"""
    user_id = current_user.get_id()
    if user_id:
        return jsonify(
            {"msg": "{} is active.".format(User.query.filter_by(id=user_id).first())}
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


@app.route("/mood", methods=["GET"])
def get_moods():
    """Gets all mood values for a particular user"""
    return jsonify(
        {
            "placeholder": "This route will soon return mood entries for a particular user"
        }
    )
