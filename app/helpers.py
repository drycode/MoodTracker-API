from flask_login import current_user

from app import db
from app.models import User


def calculate_streak_percentile():
    """Returns percentile rank of the current
    users score.
    Queries 3 integer values from the database and passes them to the
    percentileofscore helper.
        L = values in array lower than current user's best_streak
        S = values in array equal to current user's best_streak
        N = total users in database
    """
    score = current_user.best_streak
    L = db.session.query(User.best_streak).filter(User.best_streak < score).count()
    S = db.session.query(User.best_streak).filter(User.best_streak == score).count()
    N = db.session.query(User).count()

    percentile_rank = _percentileofscore(L, S, N)
    return percentile_rank


def _percentileofscore(L, S, N):
    """
    Formula for percentile rank:
    PR = (L + (S / 2)) / N
    """
    percentile_decimal = (L + (S / 2)) / N
    return round(percentile_decimal, 2) * 100
