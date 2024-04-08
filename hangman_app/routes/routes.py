import os
import secrets
from PIL import Image
import traceback
from hangman_app import db, bcrypt, app
from flask import redirect, render_template, Blueprint, flash, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from hangman_app.models.models import User
from hangman_app.forms.users_forms import SigninForm, LoginForm
from hangman_app.forms.users_modify import InquiriesUpdateForm, UpdateAccountForm, PasswordUpdateForm


bp = Blueprint("main", __name__)


@bp.route("/signin", methods=["GET", "POST"])
def signin_page():
    db.create_all()
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = SigninForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            user_name=form.user_name.data,
            email=form.email.data,
            password=hashed_password,
        )
        db.session.add(user)
        db.session.commit()
        flash("You have successfully registered! You can login", "success")
        return redirect(url_for("main.index"))
    return render_template("signin.html", title="Sign in", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main.index"))
        else:
            flash("Login failed. Check email email and password", "danger")
    return render_template("login.html", title="Log in", form=form)


@bp.route("/logout")
def logout_page():
    logout_user()
    return redirect(url_for("main.index"))

from hangman_app.email_utility import send_reset_email

@bp.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = InquiriesUpdateForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(
            "An email has been sent to you with instructions to reset your password.",
            "info",
        )
        return redirect(url_for("main.login_page"))
    return render_template("reset_request.html", title="Reset Password", form=form)

@bp.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("The request is invalid or expired", "warning")
        return redirect(url_for("main.reset_request"))
    form = PasswordUpdateForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user.password = hashed_password
        db.session.commit()
        flash("Your password has been updated! You can connect", "success")
        return redirect(url_for("main.login_page"))
    return render_template("reset_token.html", title="Reset Password", form=form)

@bp.route("/")
def index():
    return render_template("index.html")


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/profile_foto", picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

@bp.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.image.data:
            image = save_picture(form.image.data)
            current_user.image = image
        current_user.user_name = form.user_name.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("main.account"))
    elif request.method == "GET":
        form.user_name.data = current_user.user_name
        form.email.data = current_user.email


    if current_user.image:
        image = url_for("static", filename="profile_foto/" + current_user.image)
    else:
        image = url_for("static", filename="profile_foto/default.jpg")
    print("Image URL:", image)

    return render_template(
        "account.html", title="Account", form=form, image=image
)


@bp.route("/create_table")
def create_table():
    try:
        db.create_all()
        return "Progress table created successfully!", 200
    except Exception as e:
        traceback.print_exc()
        return f"An error occurred: {e}", 500


@bp.route("/delete_table")
def delete_table():
    try:
        db.drop_all()
        return "Progress table deleted successfully!", 200
    except Exception as e:
        return f"An error occurred: {e}", 500
