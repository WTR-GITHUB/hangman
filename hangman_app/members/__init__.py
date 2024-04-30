from flask import Blueprint

bp_members = Blueprint("members", __name__)

from hangman_app.members import routes