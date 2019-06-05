from flask import jsonify
from app import app


@app.route("/health")
def check_server():
    """Checks if the server is active."""
    return jsonify({"message": "Flask is up and running!"})


@app.route("/login")
def login():
    """Allows users to login"""
    pass


@app.route("/logout")
def logout():
    """Allows users to logout"""


@app.route("/mood")
def post_mood():
    """Posts a mood value to a persisted datastore"""
    pass


@app.route("/mood")
def get_moods(user_id):
    """Gets all mood values for a particular user"""
    pass
