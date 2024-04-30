from flask import current_app, render_template, request, jsonify
from flask_login import current_user, login_required
from hangman_app.game import bp_game

from hangman_app import db
from hangman_app.game_engine import HangmanGame
from hangman_app.models.sql_models import GameStats
from hangman_app.models.mongo_models import MongoStats, mongo_db
from pymongo.errors import ConnectionFailure, PyMongoError, ConfigurationError
from hangman_app.credentials_v2 import (
    MONGO_HOST,
    MONGO_PORT,
    MONGO_GAME_DB_NAME,
    MONGO_GAME_COLLECTION_NAME,
)



try:
    mongo_stats = MongoStats(
        host=MONGO_HOST,
        port=int(MONGO_PORT),
        db_name=MONGO_GAME_DB_NAME,
        collection_name=MONGO_GAME_COLLECTION_NAME,
    )
except ConnectionFailure as e:
    print("Connection failure:", str(e))
except ConfigurationError as e:
    print("Configuration failure:", str(e))
except PyMongoError as e:
    print("General failure:", str(e))


hangman_game = HangmanGame()


@bp_game.route("/game")
def game():
    return render_template("game/game.html")


@bp_game.route("/game/start", methods=["POST"])
def start_game():
    try:
        current_user_id = current_user.get_id()
    except Exception as e:
        return jsonify({"error": "Error getting user ID: " + str(e)}), 500

    if not current_user_id:
        return jsonify({"error": "User not authenticated."}), 401

    try:
        mongo_stats.delete_stats(current_user_id)
    except Exception as e:
        return jsonify({"error": "Error deleting user stats: " + str(e)}), 500

    try:
        words = mongo_db.all_words()
        word = hangman_game.random_word(words)
        mongo_stats.create_stats(current_user_id=current_user_id, word=word)
        revealed_word = hangman_game.display_word(word=word)

        return jsonify({"revealed_word": revealed_word})

    except Exception as e:
        return jsonify({"error": "Error starting game: " + str(e)}), 500


@bp_game.route("/game/check_letter", methods=["POST"])
def check_letter():
    data = request.json
    if data is None:
        return jsonify({"error": "No JSON data received"}), 400

    letter = data.get("letter")
    if letter is None:
        return jsonify({"error": "No letter provided"}), 400

    try:
        current_user_id = current_user.get_id()
    except Exception as e:
        return jsonify({"error": "Error getting user ID: " + str(e)}), 500

    if current_user_id:
        game_stats = mongo_stats.get_stats(current_user_id)
        word = game_stats.get("word")
        used_letters = game_stats.get("used_letters")
        wrong_guesses = game_stats.get("wrong_guesses")

        used_letters.append(letter)

        revealed_word = hangman_game.display_word(used_letters=used_letters, word=word)

        is_correct, wrong_guesses = hangman_game.check_guessed_letter(
            word=word, revealed_letter=letter, wrong_guesses=wrong_guesses
        )

        total_guesses = len(used_letters)

        stats_total_guesses = hangman_game.check_total_guesses(
            total_guesses=len(used_letters)
        )

        update_values = {
            "used_letters": used_letters,
            "wrong_guesses": wrong_guesses,
            "total_guesses": total_guesses,
        }

        mongo_stats.update_stats(current_user_id, update_values)

        img_path = f"game_image/pngegg{wrong_guesses}.png"

        if stats_total_guesses == True:

            return jsonify(
                {
                    "revealed_word": revealed_word,
                    "used_letters": used_letters,
                    "game_win": False,
                    "img_path": img_path,
                    "guess_word": False,
                    "revealed_word": revealed_word,
                }
            )

        if hangman_game.check_max_errors(wrong_guesses):
            mongo_stats.game_end_time(current_user_id)
            update_values = {
                "used_letters": used_letters,
                "wrong_guesses": wrong_guesses,
                "game_win": False,
            }

            mongo_stats.update_stats(current_user_id, update_values)

            return jsonify(
                {
                    "revealed_word": revealed_word,
                    "used_letters": used_letters,
                    "total_guesses": total_guesses,
                    "is_correct": is_correct,
                    "mistakes": wrong_guesses,
                    "game_over": True,
                    "game_win": False,
                    "img_path": img_path,
                    "message": "Game over! Maximum mistakes reached.",
                    "guess_word": True,
                }
            )
        if hangman_game.check_is_word_already_guessed(
            revealed_letters=used_letters, word=word
        ):
            mongo_stats.game_end_time(current_user_id)
            update_values = {
                "used_letters": used_letters,
                "wrong_guesses": wrong_guesses,
                "game_win": True,
            }
            mongo_stats.update_stats(current_user_id, update_values)
            return jsonify(
                {
                    "game_win": True,
                    "used_letters": used_letters,
                    "is_correct": is_correct,
                    "revealed_word": revealed_word,
                    "img_path": img_path,
                    "guess_word": True,
                }
            )

        return jsonify(
            {
                "revealed_word": revealed_word,
                "used_letters": used_letters,
                "total_guesses": len(used_letters),
                "is_correct": is_correct,
                "mistakes": wrong_guesses,
                "game_over": False,
                "game_win": False,
                "img_path": img_path,
                "guess_word": True,
            }
        )


@bp_game.route("/game/check_word", methods=["POST"])
def check_word():
    data = request.json
    if data is None:
        return jsonify({"error": "No JSON data received"}), 400

    guessed_word = data.get("guess")
    if guessed_word is None:
        return jsonify({"error": "No word provided"}), 400

    try:
        current_user_id = current_user.get_id()
    except Exception as e:
        return jsonify({"error": "Error getting user ID: " + str(e)}), 500

    if current_user_id:
        game_stats = mongo_stats.get_stats(current_user_id)
        word = game_stats.get("word")

        if hangman_game.check_word(guessed_word=guessed_word, word=word):
            mongo_stats.game_end_time(current_user_id)
            update_values = {
                "game_win": True,
            }
            mongo_stats.update_stats(current_user_id, update_values)
            return jsonify(
                {
                    "game_win": True,
                }
            )
        else:
            mongo_stats.game_end_time(current_user_id)
            update_values = {
                "game_win": False,
            }
            mongo_stats.update_stats(current_user_id, update_values)
            return jsonify(
                {
                    "game_win": False,
                }
            )


@bp_game.route("/game/end_game", methods=["POST"])
@login_required
def end_game():
    current_user_id = current_user.get_id()
    user = mongo_stats.collection.find_one({"user_id": current_user_id})
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
