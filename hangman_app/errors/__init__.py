from flask import Blueprint

bp_error = Blueprint("bp_error", __name__)

from hangman_app.errors import error_handlers
