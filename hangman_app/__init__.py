from flask import Flask, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Message, Mail
from hangman_app.credentials import (
    MAIL_PASSWORD,
    MAIL_USERNAME,
    POSTGRES_DB,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_USER,
)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "4654f5dfadsrfasdr54e6rae"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = MAIL_USERNAME
app.config["MAIL_PASSWORD"] = MAIL_PASSWORD

db = SQLAlchemy(app)

mail = Mail(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "signin"
login_manager.login_message_category = "info"


from hangman_app.guests.routes import bp_guests
from hangman_app.members.routes import bp_members
from hangman_app.utilities.email_utility import send_reset_email

app.register_blueprint(bp_guests)
app.register_blueprint(bp_members)

from hangman_app.models.models import User


@login_manager.user_loader
def load_user(user_id):
    db.create_all()
    return User.query.get(int(user_id))

import os
from modules import MongoDB
from hangman_app.credentials import HOST, PORT, DB_NAME, COLLECTION_NAME
from pymongo.errors import ConnectionFailure, PyMongoError, ConfigurationError

try:
    mongodb = MongoDB(
        host=HOST,
        port=int(PORT),
        db_name=DB_NAME,
        collection_name=COLLECTION_NAME,
    )
except ConnectionFailure as e:
    print("Connection failure:", str(e))
except ConfigurationError as e:
    print("Configuration failure:", str(e))
except PyMongoError as e:
    print("General failure:", str(e))


if __name__ == "__main__":
    app.run(debug=True)
