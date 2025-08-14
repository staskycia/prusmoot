from flask import render_template, url_for, request, get_flashed_messages, flash, redirect
from app.link import bp
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from app.extensions import db
from app.models import User, Link

@bp.route("/<alias>")
def link(alias):
    link = Link.query.filter_by(alias=alias).first_or_404()
    return redirect(link.target)