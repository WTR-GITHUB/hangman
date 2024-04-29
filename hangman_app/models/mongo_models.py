from datetime import datetime
from typing import Dict, Optional
from flask import current_app
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError, ConfigurationError
from hangman_app.credentials import (
    MONGO_HOST,
    MONGO_PORT,
    MONGO_DB_NAME,
    MONGO_COLLECTION_NAME,
)


class MongoDB:
    def __init__(
        self, host: str, port: int, db_name: str, collection_name: str
    ) -> None:
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def create_word_library(self) -> bool:
        try:
            with open("./hangman_app/static/words.txt", "r") as data:
                words_list = data.read().splitlines()
            for word in words_list:
                document = {"word": word}
                result = self.collection.insert_one(document)
            current_app.logger.debug("Words inserted into the database successfully.")
            return True
        except FileNotFoundError:
            current_app.logger.debug("Error: File 'words.txt' not found.")
            return False
        except Exception as error:
            current_app.logger.debug(f"Error while inserting words into the database: {str(error)}")
            return False
        
    def all_words(self) -> list[str]:
        all_words = self.collection.find({}, {"word": 1})
        word_list = [doc["word"] for doc in all_words]
        return word_list



class MongoStats:
    def __init__(
        self, host: str, port: int, db_name: str, collection_name: str
    ) -> None:
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def delete_stats(self, current_user_id: str) -> None:
        deleted_count = self.collection.delete_many({"user_id": current_user_id})
        current_app.logger.debug(
            f"Deleted {deleted_count.deleted_count} documents for user ID: {current_user_id}"
        )

    def create_stats(
        self,
        current_user_id: str,
        word: str,
        used_letters: list[str] = [],
        wrong_guesses: int = 0,
        game_end_time: datetime = None,
        game_result: bool = None,
        total_guesses: int = 0,
    ) -> None:
        game_start_data = {
            "user_id": current_user_id,
            "word": word,
            "game_started": datetime.now(),
            "used_letters": used_letters,
            "wrong_guesses": wrong_guesses,
            "game_ended": game_end_time,
            "game_win": game_result,
            "total_guesses": total_guesses,
        }
        self.collection.insert_one(game_start_data)
        current_app.logger.debug(f"Current user ID: {current_user_id}\nWord: {word}")

    def get_stats(self, current_user_id: str) -> Optional[Dict[str, any]]:
        data = self.collection.find_one({"user_id": current_user_id})
        return data

    def update_stats(
        self, current_user_id: str, update_values: Dict[str, Optional[any]]
    ) -> None:
        query = {"user_id": current_user_id}
        update_operation = {"$set": update_values}
        self.collection.update_one(query, update_operation)

    def game_end_time(self, current_user_id: str) -> None:
        self.collection.update_one(
            {"user_id": current_user_id}, {"$set": {"game_ended": datetime.now()}}
        )

try:
    mongo_db = MongoDB(
        host=MONGO_HOST,
        port=int(MONGO_PORT),
        db_name=MONGO_DB_NAME,
        collection_name=MONGO_COLLECTION_NAME,
    )
except ConnectionFailure as e:
    print("Connection failure:", str(e))
except ConfigurationError as e:
    print("Configuration failure:", str(e))
except PyMongoError as e:
    print("General failure:", str(e))