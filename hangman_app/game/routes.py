from flask import render_template, request, jsonify
from hangman_app.game import bp_game
from hangman_app import mongodb
from hangman_app.models.game_models import Word

word  = Word()
USED_LETTERS = []

@bp_game.route("/game")
def game():
    return render_template("game/game.html")


@bp_game.route("/game/word")
def word_setup():
    success = mongodb.create_word_library()
    if success:
        return "Word library successfully created and inserted into the database."
    else:
        return "Error occurred while creating word library."


@bp_game.route("/game/start", methods=["POST"])
def start_game():
    revealed_word = word.display_word(USED_LETTERS)
    print(revealed_word)
    return jsonify({"revealed_word": revealed_word})


@bp_game.route('/game/check_letter', methods=['POST'])
def check_letter():
    data = request.json
    letter = data['letter']
    print(letter)
    updated_word, is_correct = word.process_letter_guess(letter, USED_LETTERS)
    return jsonify({'updated_word': updated_word, 'is_correct': is_correct, 'used_letters': USED_LETTERS})

