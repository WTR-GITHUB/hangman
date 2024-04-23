from datetime import datetime
from flask import current_app, jsonify, session
from flask_login import current_user
from pymongo import MongoClient
from hangman_app import mongodb
from hangman_app.credentials import (
    MONGO_HOST,
    MONGO_PORT,
    MONGO_GAME_COLLECTION_NAME,
    MONGO_GAME_DB_NAME,
)


class HangmanGame:
    def __init__(self):
        self.word = self.random_word().upper()
        self.used_letters = []
        self.wrong_guesses = 0
        self.total_guesses = 0
        self.mongo_client = MongoClient(MONGO_HOST, MONGO_PORT)
        self.mongo_db = self.mongo_client[MONGO_GAME_DB_NAME]
        self.mongo_collection = self.mongo_db[MONGO_GAME_COLLECTION_NAME]

    def random_word(self) -> str:
        random_word_document = mongodb.collection.aggregate([{"$sample": {"size": 1}}])
        random_word = random_word_document.next()["word"]
        return random_word

    def display_word(self, used_letters: list, word: str) -> str:
        revealed_word = ""
        for char in word:
            if char in used_letters:
                revealed_word += char + " "
            else:
                revealed_word += "_ "
        return revealed_word.strip()

    def check_is_word_already_guessed(
        self, revealed_letters: list[str], word: str
    ) -> bool:
        unique_word_letters = set(word)
        return all(letter in revealed_letters for letter in unique_word_letters)

    def check_guessed_letter(self, revealed_letter: str, word: str) -> bool:
        unique_word_letters = set(word)
        if revealed_letter not in unique_word_letters:
            return False
        else:
            return True

    def start_game(self):
        current_user_id = current_user.get_id()
        deleted_count = self.mongo_collection.delete_many({"user_id": current_user_id})
        current_app.logger.debug(
            f"Deleted {deleted_count.deleted_count} documents for user ID: {current_user_id}"
        )

        revealed_word = self.display_word(self.used_letters, self.word)
        game_start_data = {
            "user_id": current_user_id,
            "word": self.word,
            "game_started": datetime.now(),
            "used_letters": self.used_letters,
            "wrong_guesses": self.wrong_guesses,
            "game_ended": None,
        }
        self.mongo_collection.insert_one(game_start_data)
        current_app.logger.debug(
            f"Current user ID: {current_user_id}\nWord: {self.word}\nRevealed word: {revealed_word}"
        )
        return revealed_word

    def check_letter(self, letter: str):
        current_user_id = current_user.get_id()
        user = self.mongo_collection.find_one({"user_id": current_user_id})
        if not user:
            current_app.logger.debug(f"Current user ID: {current_user_id} not found")
            return jsonify({"error": "Unauthorized user"}), 403

        word = user.get("word", "")
        used_letters = user.get("used_letters", [])
        used_letters.append(letter.upper())
        wrong_guesses = user.get("wrong_guesses", 0)
        total_guesses = len(used_letters)
        revealed_word = self.display_word(used_letters, word)
        is_correct = None

        if not self.check_guessed_letter(letter.upper(), word):
            wrong_guesses += 1
            is_correct = False
        else:
            is_correct = True

        self.mongo_collection.update_one(
            {"user_id": current_user_id},
            {
                "$set": {
                    "used_letters": used_letters,
                    "wrong_guesses": wrong_guesses,
                }
            },
        )

        img_path = f"game_image/pngegg{wrong_guesses}.png"

        if wrong_guesses >= 6:
            self.end_time()
            current_app.logger.debug(
                f"{revealed_word},{used_letters},{total_guesses},{is_correct},{wrong_guesses}"
            )
            self.mongo_collection.update_one(
                {"user_id": current_user_id},
                {"$set": {"game_win": False, "total_guesses": len(used_letters)}},
            )
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
                }
            )

        if total_guesses >= 10:
            current_app.logger.debug(
                f"{revealed_word},{used_letters},{total_guesses},{is_correct},{wrong_guesses}"
            )
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
                    "message": "Guess word! Maximum guesses reached.",
                }
            )

        if self.check_is_word_already_guessed(used_letters, word):
            self.mongo_collection.update_one(
                {"user_id": current_user_id}, {"$set": {"game_win": True}}
            )
            current_app.logger.debug(
                f"{revealed_word},{used_letters},{total_guesses},{wrong_guesses}"
            )
            self.mongo_collection.update_one(
                {"user_id": current_user_id},
                {"$set": {"game_win": True, "total_guesses": len(used_letters)}},
            )
            return jsonify(
                {
                    "game_win": True,
                    "used_letters": used_letters,
                    "is_correct": is_correct,
                    "revealed_word": revealed_word,
                }
            )

        current_app.logger.debug(
            f"{revealed_word},{used_letters},{total_guesses},{is_correct},{wrong_guesses}"
        )
        return jsonify(
            {
                "revealed_word": revealed_word,
                "used_letters": used_letters,
                "total_guesses": total_guesses,
                "is_correct": is_correct,
                "mistakes": wrong_guesses,
                "game_over": False,
                "game_win": False,
                "img_path": img_path,
            }
        )

    def end_time(self):
        current_user_id = current_user.get_id()
        user = self.mongo_collection.find_one({"user_id": current_user_id})
        if not user:
            return jsonify({"error": "Unauthorized user"}), 403
        self.mongo_collection.update_one(
            {"user_id": current_user_id}, {"$set": {"game_ended": datetime.now()}}
        )

        return jsonify({"message": "Game ended successfully"})

    def check_word(self, guessed_word: str):
        current_user_id = current_user.get_id()
        user = self.mongo_collection.find_one({"user_id": current_user_id})
        if not user:
            current_app.logger.debug(f"Current user ID: {current_user_id} not found")
            return jsonify({"error": "Unauthorized user"}), 403
        word = user.get("word", "")
        if guessed_word.upper() == word:
            self.mongo_collection.update_one(
                {"user_id": current_user_id}, {"$set": {"game_win": True}}
            )
            return jsonify({"is_correct": True})

        else:
            return jsonify({"is_correct": False})
