from flask import url_for
from hangman_app import mail
from flask_mail import Message, Mail

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        "Password update request",
        sender="el@pastas.lt",
        recipients=[user.email],
    )
    msg.body = f"""Click the link to reset your password:
    {url_for('main.reset_token', token=token, _external=True)}
    If you did not make this request, do nothing and the password will not be changed.
    """
    print(msg)
    mail.send(msg)