from flask import render_template, url_for

from app.main import bp

@bp.route("/")
def home():
    return render_template("home.html")

@bp.route("/about")
def about():
    return render_template("about.html")

@bp.route("/edition/<int:year>")
def edition(year):
    return render_template(f"editions/{year}.html")

@bp.route("/files")
def files():
    return render_template("files.html")

@bp.route("/news")
def news():
    return render_template("news.html")

@bp.route("/post/<title>")
def post(title):
    return render_template("post.html")

from app.extensions import mail
from flask_mail import Message

from flask import current_app

@bp.route("/mail")
def mailer():
    try:
        msg = Message(
            subject='Hello from Flask',
            recipients=['stanislaw.stask@gmail.com']
        )
        msg.body = "Testing from Flask"
        mail.send(msg)
        return "Message sent!"
    except Exception as e:
        return f"Failed to send mail: {e}"