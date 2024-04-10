from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email
from flask_wtf.file import FileField, FileAllowed
from hangman_app import app
from hangman_app.models.sql_models import User
from flask_login import current_user

class UpdateAccountForm(FlaskForm):
    user_name = StringField('Name', [DataRequired()])
    email = StringField('E-mail', [DataRequired()])
    image = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def check_name(self, user_name):
        if user_name.data != current_user.user_name:
            user = User.query.filter_by(user_name=user_name.data).first()
            if user:
                raise ValidationError('This name has been used. Choose another.')

    def check_email(self, email):
        if email.data != current_user.email: 
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This e-mail email address is used. Choose another.')

class InquiriesUpdateForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Get')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account registered with this email. postal address. Sign up.')
        
class PasswordUpdateForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirmed_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')