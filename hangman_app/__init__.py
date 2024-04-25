from flask import Flask, current_app
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
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
app.secret_key = "4654f5dfadsrfasdr54e6rae"
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


from hangman_app.guests import bp_guests
from hangman_app.members import bp_members
from hangman_app.game import bp_game
from hangman_app.errors import bp_error

app.register_blueprint(bp_guests)
app.register_blueprint(bp_members)
app.register_blueprint(bp_game)
app.register_blueprint(bp_error)


from hangman_app.models.sql_models import User


@login_manager.user_loader
def load_user(user_id):
    current_app.logger.debug(f"Current user ID: {user_id}")
    return User.query.get(int(user_id))


if __name__ == "__main__":
    app.run(debug=True)
