from collections import OrderedDict
from datetime import datetime

import pytest
from pytest import mark

from app.models import User, MoodEntry


user_1 = User(
    id=234,
    username="testuser123",
    email="test@testuser.com",
    current_streak=34,
    best_streak=35,
)

user_1.set_password("password1")


def test_User():
    assert repr(user_1) == "<User testuser123>"


def test_User_getters():
    assert user_1.get_best_streak() == 35
    assert user_1.get_current_streak() == 34
    assert user_1.get_id() == "234"


def test_User_instance():
    assert isinstance(user_1, object) is True


def test_secure_hashed_password():
    print(user_1.password_hash)
    assert (
        user_1.password_hash
        != "pbkdf2:sha256:150000$dPxxc0MU$7a7c903936dc2ebaccdb4db62bc6e22ecb4672c4e8fb81ed99c96e91bb708938"
    )


def test_check_password():
    assert user_1.check_password("password1") is True


def test_user_asdict():
    assert user_1.asdict() == OrderedDict(
        [
            ("id", 234),
            ("username", "testuser123"),
            ("email", "test@testuser.com"),
            ("current_streak", 34),
            ("best_streak", 35),
        ]
    )


mood_1 = MoodEntry(
    id=1, user_id=234, mood_score=6, timestamp=datetime(2019, 6, 8, 21, 56, 5, 314037)
)


def test_MoodEntry():
    assert repr(mood_1) == "<MoodEntry Score:6 Time:2019-06-08 21:56:05.314037>"


def test_mood_getters():
    assert mood_1.get_timestamp() == datetime(2019, 6, 8, 21, 56, 5, 314037)


def test_mood_asdict():
    assert mood_1.asdict() == OrderedDict(
        [
            ("id", 1),
            ("user_id", 234),
            ("mood_score", 6),
            ("timestamp", "Jun 08 2019 21:56:05"),
        ]
    )

