from flask import render_template, url_for, request, get_flashed_messages, flash, redirect
from app.auth import bp
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from app.extensions import db
from app.models import User

@bp.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("panel.home"))
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if not (email and password):
            flash("Both fields are required!", category="error")
            return render_template("auth/login.html")
        user = User.query.filter_by(email=email.lower()).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect(url_for("panel.home"))
        else:
            flash("Incorrect email and/or password!", category="error")
    return render_template("auth/login.html")

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were securely logged out!", "success")
    return redirect("login")

from datetime import datetime, timezone, timedelta