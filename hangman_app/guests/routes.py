from sqlalchemy.exc import IntegrityError
import traceback
from hangman_app import db, bcrypt
from flask import current_app, redirect, render_template, flash, request, url_for
from flask_login import current_user, login_user
from hangman_app.models.sql_models import User
from hangman_app.forms.users_forms import SigninForm, LoginForm
from hangman_app.guests import bp_guests
from hangman_app.forms.users_modify import (
    InquiriesUpdateForm,
    PasswordUpdateForm,
)

@bp_guests.route("/signin", methods=["GET", "POST"])
def signin_page():
    if current_user.is_authenticated:
        return redirect(url_for("members.index"))
    
    form = SigninForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(
            user_name=form.user_name.data,
            email=form.email.data,
            password=hashed_password
        )
        db.session.add(user)
        try:
            db.session.commit()
            flash("You have successfully registered! You can now login.", "success")
            return redirect(url_for("guests.login_page"))
        except Exception as e:
            db.session.rollback()
            flash("Registration failed. Please try again.", "danger")
    else:
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                current_app.logger.debug(f"Error in {fieldName}: {err}")

    return render_template("guests/signin.html", title="Sign in", form=form)





@bp_guests.route("/login", methods=["GET", "POST"])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for("guests.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get("next")
            return (
                redirect(next_page)
                if next_page
                else redirect(url_for("guests.index"))
            )
        else:
            flash("Login failed. Check email email and password", "danger")
    return render_template("guests/login.html", title="Log in", form=form)


@bp_guests.route("/")
def index():
    if current_user.is_authenticated:
        return render_template("members/index.html")
    else:
        return render_template("guests/index.html")


from hangman_app.utilities.email_utility import send_reset_email


@bp_guests.route("/reset_password", methods=["GET", "POST"])
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
        return redirect(url_for("guests.login_page"))
    return render_template(
        "guests/reset_request.html", title="Reset Password", form=form
    )


@bp_guests.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("The request is invalid or expired", "warning")
        return redirect(url_for("guests.reset_request"))
    form = PasswordUpdateForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user.password = hashed_password
        db.session.commit()
        flash("Your password has been updated! You can connect", "success")
        return redirect(url_for("guests.login_page"))
    return render_template("guests/reset_token.html", title="Reset Password", form=form)


@bp_guests.route("/create_table")
def create_table():
    try:
        db.create_all()
        return "Progress table created successfully!", 200
    except Exception as e:
        traceback.print_exc()
        return f"An error occurred: {e}", 500


@bp_guests.route("/delete_table")
def delete_table():
    try:
        db.drop_all()
        return "Progress table deleted successfully!", 200
    except Exception as e:
        return f"An error occurred: {e}", 500
