from flask import Blueprint

bp_game = Blueprint("game", __name__, template_folder='templates')

from hangman_app.game import routes