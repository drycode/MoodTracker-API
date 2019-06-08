from datetime import datetime, timedelta

import pytest
from pytest import mark, raises

from app.models import _check_should_update
from app.helpers import _percentileofscore


@mark.parametrize(
    "L, S, N, expected",
    {
        (3, 4, 5, 100),
        (74, 13, 134, 60),
        (3234895, 4344, 500493482, 1),
        (5, 5, 10, 75),
        (0, 0, 1, 0),
    },
)
def test__percentileofscore(L, S, N, expected):
    assert _percentileofscore(L, S, N) == expected


def test__percentileofscore_errors():
    with pytest.raises(ZeroDivisionError):
        _percentileofscore(0, 0, 0)


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
