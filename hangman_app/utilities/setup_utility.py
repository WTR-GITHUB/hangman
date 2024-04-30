import time
from hangman_app import db
from hangman_app.models.mongo_models import mongo_db
from flask import current_app
from hangman_app.credentials import MONGO_DB_NAME




def create_database_tables():
    retries = 3
    for _ in range(retries):
        try:
            db.create_all()
            break
        except Exception as e:
            current_app.logger.debug(
                f"An error occurred while creating database tables: {str(e)}"
            )
            time.sleep(5)


def delete_mongo_database():
    try:
        mongo_db.client.drop_database(name_or_database=MONGO_DB_NAME)
        current_app.logger.debug("Existing MongoDB database dropped successfully.")
    except Exception as e:
        current_app.logger.debug(
            f"An error occurred while dropping existing MongoDB database: {str(e)}"
        )


def import_words_to_db():
    try:
        delete_mongo_database()
        import_words = mongo_db.create_word_library()
        if import_words:
            current_app.logger.debug(
                "Word library successfully created and inserted into the database."
            )
        else:
            raise Exception("Failed to create word library")
    except Exception as e:
        current_app.logger.debug(
            f"An error occurred during word library creation: {str(e)}"
        )
