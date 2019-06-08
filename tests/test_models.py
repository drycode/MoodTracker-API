from datetime import datetime, timedelta

import pytest
from pytest import mark, raises

from app.helpers import _percentileofscore
from app.models import User, MoodEntry, _check_should_update


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
