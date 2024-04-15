from flask import flash, render_template, request, jsonify, session
from hangman_app.game import bp_game
from hangman_app import mongodb
from hangman_app.models.game_models import Word

word = Word()
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
    global USED_LETTERS
    USED_LETTERS = []
    session["wrong_guesses"] = 0
    revealed_word = word.display_word(USED_LETTERS)
    return jsonify({"revealed_word": revealed_word, "total_pressed_letters": session["total_pressed_letters"]})


@bp_game.route("/game/check_letter", methods=["POST"])
def check_letter():
    global USED_LETTERS
    data = request.json
    if data is None:
        return jsonify({"error": "No JSON data received"}), 400

    letter = data.get("letter")
    if letter is None:
        return jsonify({"error": "No letter provided"}), 400

    is_correct = word.process_letter_guess(letter, USED_LETTERS)
    revealed_word = word.display_word(USED_LETTERS)

    if not is_correct:
        session['wrong_guesses'] = session.get('wrong_guesses', 0) + 1
        if session['wrong_guesses'] == 6:
            return jsonify({"revealed_word": revealed_word, "is_correct": False, "game_over": True})
    
    all_letters_guessed = word.check_all_guessed_letters(USED_LETTERS)
    print(all_letters_guessed)

    return jsonify({"revealed_word": revealed_word, "is_correct": is_correct, "game_over": False, 'all_letters_guessed': all_letters_guessed })


@bp_game.route("/game/check_word", methods=["POST"])
def check_word():
    global USED_LETTERS
    data = request.json
    if data is None:
        return jsonify({"error": "No JSON data received"}), 400

    guessed_word = data.get("guess")
    if guessed_word is None:
        return jsonify({"error": "No word provided"}), 400

    if guessed_word == word.word:
        return jsonify({"is_correct": True})
    else:
        return jsonify({"is_correct": False})
