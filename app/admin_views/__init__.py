from flask import flash, redirect, url_for, request

from flask_login import current_user

from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose

from app.models import User, Post, Link, Tag, File

from app.extensions import db, admin

from werkzeug.security import generate_password_hash

class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login"))
    
class SecureBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login"))
    
class PasswordHashView(SecureBaseView):
    @expose('/', methods=["POST", "GET"])
    def index(self):
        if request.method == "POST":
            password = request.form.get("password")
            flash(generate_password_hash(password))
            return redirect(url_for("user.index_view"))
        return self.render("admin/password_reset.html")
    
class PostAdmin(SecureModelView):
    column_list = ("title_en", "title_pl", "author")
    column_labels = dict(author="Author")
    form_columns = ("title_en", "title_pl", "sample_en", "sample_pl", "content_en", "content_pl", "author", "created_at", "tags")
 
from wtforms.fields import StringField
from wtforms.widgets import Input 
 
class ColorInput(Input):
    input_type = 'color'

class ColorField(StringField):
    widget = ColorInput()
    
class TagAdmin(SecureModelView):
    form_overrides = {
        'color': ColorField
    }


def init_admin_views():
    admin.add_view(SecureModelView(User, db.session, name="Users"))
    admin.add_view(PostAdmin(Post, db.session, name="Posts"))
    admin.add_view(TagAdmin(Tag, db.session, name="Tags"))
    admin.add_view(SecureModelView(Link, db.session, endpoint="linkadmin", url="/linkadmin", name="Links"))
    admin.add_view(SecureModelView(File, db.session, name="Files"))
    admin.add_view(PasswordHashView(name="Generate Password Hash"))