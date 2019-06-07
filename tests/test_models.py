from datetime import datetime, timedelta
from app.models import User, MoodEntry, _verify_mood_range, _check_should_update
from app.routes import _percentileofscore
from pytest import mark, raises
import pytest


@mark.parametrize(
    "input, expected",
    {
        (datetime.utcnow(), "Today"),
        (datetime.utcnow() - timedelta(days=1), "Yesterday"),
        (datetime.utcnow() - timedelta(days=2), "Reset"),
        (datetime.utcnow() - timedelta(days=2), "Reset"),
        (None, "Yesterday"),
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


@mark.parametrize(
    "scores_arr, score, expected",
    {
        ((1, 3, 2, 6, 8, 9, 10), 5, 43),
        ((84, 299, 10384, 288, 134, 123, 2374, 18, 1239, 1237, 4), 670, 64),
        ((1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 100), 2, 93),
        ((0, 0, 0, 6, 8, 9, 10), 0, 21),
    },
)
def test__percentileofscore(scores_arr, score, expected):
    assert _percentileofscore(list(scores_arr), score) == expected
