from datetime import datetime, timedelta
from app.models import User, MoodEntry, _verify_mood_range, _check_should_update
from pytest import mark, raises
import pytest


@mark.parametrize(
    "input, expected",
    {
        (datetime.utcnow(), "Today"),
        (datetime.utcnow() - timedelta(days=1), "Yesterday"),
        (datetime.utcnow() - timedelta(days=2), "Reset"),
        (datetime.utcnow() - timedelta(days=2), "Reset"),
        (None, False),
    },
)
def test__check_should_update(input, expected):
    assert _check_should_update(input) == expected


def test__check_should_update_errors():
    with pytest.raises(OverflowError):
        _check_should_update(
            datetime.utcnow() - timedelta(days=99979797979797979797979797979)
        )


@mark.parametrize(
    "input, expected",
    {
        (1.0, TypeError),
        ("0", TypeError),
        (-01.345, TypeError),
        (1.0, TypeError),
        (11, ValueError),
        (-1, ValueError),
        (
            1000000000000000000000000000000000000000000000000000000000000000000000000000000,
            ValueError,
        ),
    },
)
def test__verify_mood_range(input, expected):
    with pytest.raises(expected):
        _verify_mood_range(input)
