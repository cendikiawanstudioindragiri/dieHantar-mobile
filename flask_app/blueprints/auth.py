from flask import Blueprint, render_template, redirect, url_for, flash, request
from .forms import LoginForm, RegisterForm

bp = Blueprint("auth", __name__, template_folder="../templates")


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # TODO: authenticate user against backend/DB
        flash("Logged in (stub)", "success")
        return redirect(url_for("dashboard.index"))
    return render_template("auth/login.html", form=form)


@bp.route("/logout")
def logout():
    # TODO: implement logout logic
    flash("Logged out (stub)", "info")
    return redirect(url_for("auth.login"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # TODO: save new user to DB
        flash("Account created (stub)", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)
