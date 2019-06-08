from flask import jsonify
from app import app, db


@app.errorhandler(401)
def handle_unauthorized_error(error):
    return jsonify({"errors": {error.name: error.description}}), 401


@app.errorhandler(404)
def handle_not_found_error(error):
    return jsonify({"errors": {error.name: error.description}}), 404


@app.errorhandler(422)
def handle_validation_error(error):
    exc = error.exc
    return jsonify({"errors": exc.messages}), 422


@app.errorhandler(500)
def handle_internal_error(error):
    db.session.rollback()
    return (
        jsonify(
            {
                "errors": {
                    "An unexpected error has occurred that will likely require an administrator. Sorry for the inconvenience!"
                }
            }
        ),
        500,
    )
