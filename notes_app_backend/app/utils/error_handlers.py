from flask import Blueprint
from werkzeug.exceptions import HTTPException
from marshmallow import ValidationError
from .responses import error

errors_blp = Blueprint("Errors", __name__)


def register_error_handlers(app):
    """Register global error handlers producing themed responses."""

    @app.errorhandler(ValidationError)
    def handle_validation_error(err: ValidationError):
        return error("Validation error", status_code=400, errors=err.messages)

    @app.errorhandler(HTTPException)
    def handle_http_exception(err: HTTPException):
        message = err.description if hasattr(err, "description") else str(err)
        return error(message or "HTTP error", status_code=err.code or 500)

    @app.errorhandler(Exception)
    def handle_uncaught_exception(err: Exception):
        # In production you would not expose err details; here keep it generic
        return error("Internal server error", status_code=500)
