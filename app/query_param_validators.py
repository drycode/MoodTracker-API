"""Use of Webargs to validate incoming query parameters on routes."""

from webargs import fields

user_args = {
    "username": fields.Str(required=True),
    "email": fields.Email(required=True),
    "password": fields.Str(validate=lambda p: len(p) >= 6),
}

mood_args = {
    "mood_score": fields.Int(
        required=True, validate=lambda mood: 0 < mood and mood < 10
    )
}
