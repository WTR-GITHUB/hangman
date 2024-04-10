import os
from pymongo import MongoClient


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
                print(f"Inserted document with ID: {result.inserted_id}")
                print(f"This word was inserted into the database: {document}")
            return True
        except FileNotFoundError:
            print("Error: File 'words.txt' not found.")
            return False
        except Exception as error:
            print(f"Error: {error}")
            return False

