from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config


APP = Flask(__name__)
APP.config.from_object(Config)

DB = SQLAlchemy(APP)
MIGRATE = Migrate(APP, DB)


@APP.route("/health")
def check_server():
    """Checks if the server is active."""
    return jsonify({"message": "Flask is up and running!"})


@APP.route("/login")
def login():
    """Allows users to login"""
    pass


@APP.route("/logout")
def logout():
    """Allows users to logout"""


@APP.route("/mood")
def post_mood():
    """Posts a mood value to a persisted datastore"""
    pass


@APP.route("/mood")
def get_moods(user_id):
    """Gets all mood values for a particular user"""
    pass


if __name__ == "__main__":
    APP.config["DEBUG"] = True
    APP.run()
