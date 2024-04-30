from flask import Blueprint

bp_guests = Blueprint("guests", __name__, template_folder='templates')

from hangman_app.guests import routes