from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from flask_login import LoginManager
from app.models import User

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "You need to login with an active account before accesing this page!"
login_manager.login_message_category = "error"

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

from flask_mail import Mail
mail = Mail()

from flask_admin import Admin, AdminIndexView
from flask_login import current_user
from flask import flash, url_for, redirect

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login"))

admin = Admin(name='PrusMoot Admin', template_mode='bootstrap3', index_view=MyAdminIndexView())