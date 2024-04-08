from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, PasswordField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from hangman_app import app


class SigninForm(FlaskForm):
    user_name = StringField("Name", [DataRequired()])
    email = StringField("E-mail", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    confirmed_password = PasswordField(
        "Confirm password", [EqualTo("password", "Pasword does not match.")]
    )
    submit = SubmitField("Sig in")

    def check_name(self, user_name):
        user = app.User.query.filter_by(user_name=user_name.data).first()
        if user:
            raise ValidationError("This name has already taken pick another one.")

    def check_email(self, email):
        user = app.User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email has already taken pick another one.")


class LoginForm(FlaskForm):
    email = StringField("E-mail", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Log in")
