from hangman_app import db, app
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column("name", db.String(20), unique=True, nullable=False)
    email = db.Column("e-mail",db.String(120), unique=True, nullable=False)
    image = db.Column(db.String(120), unique=False, default="default.jpg")
    password = db.Column("password", db.String(60), unique=False, nullable=False)

    def get_reset_token(self):
        s = Serializer(app.config["SECRET_KEY"])
        return s.dumps({"user_id": self.id})
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config["SECRET_KEY"])
        try:
            print(s.loads(token))
            user_id = s.loads(token, max_age=1800)["user_id"]
        except:
            return None
        return User.query.get(user_id)
    
class GameStats(db.Model):
    __tablename__ = "game_stats"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    game_result = db.Column(db.Boolean, nullable=False)
    total_letters_guessed = db.Column(db.Integer, nullable=False)
    game_start = db.Column(db.DateTime, nullable=False, default=datetime.now)
    game_end = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"GameStats(user_id={self.user_id}, game_result={self.game_result}, " \
               f"total_letters_guessed={self.total_letters_guessed}, " \
               f"game_started={self.game_start}, " \
               f"game_ended={self.game_end})"