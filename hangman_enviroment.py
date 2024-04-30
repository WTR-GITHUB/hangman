import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import credentials from environment variables
MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")

MONGO_HOST = os.environ.get("MONGO_HOST")
MONGO_PORT = os.environ.get("MONGO_PORT")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME")
MONGO_COLLECTION_NAME = os.environ.get("MONGO_COLLECTION_NAME")

MONGO_GAME_DB_NAME = os.environ.get("MONGO_GAME_DB_NAME")
MONGO_GAME_COLLECTION_NAME = os.environ.get("MONGO_GAME_COLLECTION_NAME")

# Your application code goes here
