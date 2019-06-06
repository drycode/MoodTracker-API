"""
This module will store all necessary configuration or import statments
for the flask application.
"""
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Config variables for flask application"""

    SECRET_KEY = os.environ.get("SECRET_KEY") or "temp-secret-key"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "sqlite.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
