from flask import current_app, render_template, request, jsonify
from flask_login import current_user, login_required
from hangman_app.game import bp_game
from hangman_app import mongodb, db
from hangman_app.models.game_models import HangmanGame
from hangman_app.models.sql_models import GameStats

hangman_game = HangmanGame()


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
    revealed_word = hangman_game.start_game()
    return jsonify({"revealed_word": revealed_word})


@bp_game.route("/game/check_letter", methods=["POST"])
def check_letter():
    data = request.json
    if data is None:
        return jsonify({"error": "No JSON data received"}), 400

    letter = data.get("letter")
    if letter is None:
        return jsonify({"error": "No letter provided"}), 400

    return hangman_game.check_letter(letter)


@bp_game.route("/game/check_word", methods=["POST"])
def check_word():
    data = request.json
    if data is None:
        return jsonify({"error": "No JSON data received"}), 400

    guessed_word = data.get("guess")
    if guessed_word is None:
        return jsonify({"error": "No word provided"}), 400

    return hangman_game.check_word(guessed_word)


@bp_game.route("/game/end_game", methods=["POST"])
@login_required
def end_game():
    current_user_id = current_user.get_id()
    user = hangman_game.mongo_collection.find_one({"user_id": current_user_id})
    if not user:
        current_app.logger.debug(f"Current user ID: {current_user_id} not found")
        return jsonify({"error": "Unauthorized user"}), 403

    current_app.logger.debug(
        f"{current_user_id},{user.get('total_guesses')},{user.get('game_started')},{user.get('game_ended')},{user.get('game_win')}"
    )

    game_stats = GameStats(
        user_id=current_user_id,
        game_result=user.get("game_win"),
        total_letters_guessed=user.get("total_guesses"),
        game_start=user.get("game_started"),
        game_end=user.get("game_ended"),
    )

    db.session.add(game_stats)
    db.session.commit()

    return jsonify({"message": "Game result saved successfully"}), 200
