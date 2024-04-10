import os
import secrets
from PIL import Image
from hangman_app import db, app
from flask import redirect, render_template, flash, request, url_for
from flask_login import current_user, login_required, logout_user
from hangman_app.forms.users_modify import (
    UpdateAccountForm,
)
from hangman_app.members import bp_members
from hangman_app.guests import bp_guests


@bp_members.route("/logout")
def logout_page():
    logout_user()
    return redirect(url_for("guests.index"))


@bp_members.route("/")
def index():
    if not current_user.is_authenticated:
        return redirect(url_for("guests.index"))
    else:
        return render_template("members/index.html")


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/profile_foto", picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn  # Return the filename instead of the Image object


@bp_members.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.image.data:
            image_filename = save_picture(form.image.data)
            current_user.image = (
                image_filename  # Assign the filename to current_user.image
            )

        current_user.user_name = form.user_name.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("members.account"))

    elif request.method == "GET":
        form.user_name.data = current_user.user_name
        form.email.data = current_user.email

    image = url_for("static", filename=("profile_foto/" + str(current_user.image)))
    return render_template("members/account.html", title="Account", form=form, image=image)
