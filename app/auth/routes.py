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

@bp.route("/password_change", methods=["POST", "GET"])
@login_required
def password_change():
    if not current_user.force_password_change:
        return redirect(url_for("panel.home"))
    
    if request.method == "POST":
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_new_password = request.form.get("confirm_new_password")
        
        if not current_password or not new_password or not confirm_new_password:
            flash("All fields are required!", "error")
            return render_template("auth/reset.html")
        
        if not check_password_hash(current_user.password, current_password):
            flash("Wrong current password!", "error")
            return render_template("auth/reset.html")
        
        if new_password != confirm_new_password:
            flash("Passwords do not match!", "error")
            return render_template("auth/reset.html")
        
        if new_password == current_password:
            flash("New password must be different!", "error")
            return render_template("auth/reset.html")
        
        current_user.password = generate_password_hash(new_password)
        current_user.force_password_change = False
        db.session.commit()
        
        flash("Password was changed!", "success")
        return redirect(url_for("auth.logout"))
    
    flash("For security reasons, you need to change your password!", "warning")
    return render_template("auth/reset.html")

from datetime import datetime, timezone, timedelta