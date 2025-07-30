from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from flask_login import LoginManager
from app.models.user import User

login_manager = LoginManager()
login_manager.login_view = "main.hi"
login_manager.login_message = "TODO"
login_manager.login_message_category = "error"

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

from flask_mail import Mail
mail = Mail()