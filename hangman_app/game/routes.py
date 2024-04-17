from datetime import datetime
from flask import render_template, request, jsonify, session
from flask_login import current_user, login_required
from hangman_app.game import bp_game
from hangman_app import mongodb, db
from hangman_app.models.game_models import Word
from hangman_app.models.sql_models import GameStats

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
    session['game_start_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    return jsonify({"revealed_word": revealed_word})


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
    img_path = f"game_image/pngegg{session['wrong_guesses']}.png"
    if session['wrong_guesses'] >= 6:
        return jsonify({
            "revealed_word": revealed_word,
            "is_correct": False,
            "game_over": True,
            "img_path": img_path
        })

    all_letters_guessed = word.check_all_guessed_letters(USED_LETTERS)

    return jsonify({
        "revealed_word": revealed_word,
        "is_correct": is_correct,
        "game_over": False,
        "img_path": img_path,
        'all_letters_guessed': all_letters_guessed
    })


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

@bp_game.route("/game/end_game", methods=["POST"])
@login_required
def end_game():
    data = request.json
    game_result = data.get("game_result")
    print(game_result)
    if not data:
        return jsonify({"error": "No JSON data received"}), 400
    total_letters_guessed = data.get("total_letters_guessed")
    start_time = session.get('game_start_time')
    if not start_time:
        return jsonify({"error": "Game start time not found in session"}), 400
    if game_result is None or total_letters_guessed is None:
        return jsonify({"error": "Missing game result or total letters guessed"}), 400

    user_id = current_user.id
    start_time = session.get("game_start_time")
    end_time = datetime.now()

    if not start_time:
        return jsonify({"error": "Game start time not found in session"}), 400


    if isinstance(start_time, str):
        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
    print(user_id)
    print(game_result)
    print(total_letters_guessed)
    print(start_time)
    print(end_time)

    game_stats = GameStats(
        user_id=user_id,
        game_result=game_result,
        total_letters_guessed=total_letters_guessed,
        game_start=start_time,
        game_end=end_time
    )

    db.session.add(game_stats)
    db.session.commit()

    return jsonify({"message": "Game result saved successfully"}), 200