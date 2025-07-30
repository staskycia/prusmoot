from app.extensions import db

from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_picture = db.Column(db.String(50), nullable=False, default="empty.png")
    
    email_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    
    can_post = db.Column(db.Boolean, nullable=False, default=False)
    can_manage_links = db.Column(db.Boolean, nullable=False, default=False)
    
    password = db.Column(db.String(128), nullable=False)
    
    def __repr__(self):
        return "USER {self.email}"