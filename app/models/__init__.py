from app.extensions import db
from flask_login import UserMixin

from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    profile_picture = db.Column(db.String(50), nullable=False, default="empty")
    
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    
    active = db.Column(db.Boolean, nullable=False, default=True)
    force_password_change = db.Column(db.Boolean, nullable=False, default=False)
    
    password = db.Column(db.String(255), nullable=False)
    
    posts = db.relationship("Post", back_populates="author")
    
    def __repr__(self):
        return f"{self.first_name} {self.last_name} [{self.email}]"

class PostTags(db.Model):
    __tablename__ = "post_tags"
    id = db.Column(db.Integer, primary_key=True)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))

class Tag(db.Model):
    __tablename__ = "tag"
    
    id = db.Column(db.Integer, primary_key=True)
    
    name_en = db.Column(db.String(50), nullable=False)
    name_pl = db.Column(db.String(50), nullable=False)
    
    color = db.Column(db.String(20), nullable=False)
    
    posts = db.relationship("Post", secondary=PostTags.__table__, back_populates="tags")
    
    def __repr__(self):
        return f"{self.name_en} ({self.name_pl})"

class Post(db.Model):
    __tablename__ = "post"
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    title_en = db.Column(db.String(100), nullable=False)
    title_pl = db.Column(db.String(100), nullable=False)
    
    sample_en = db.Column(db.Text)
    sample_pl = db.Column(db.Text)
    
    content_en = db.Column(db.Text)
    content_pl = db.Column(db.Text)
    
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    author = db.relationship("User", back_populates="posts")
    
    tags = db.relationship("Tag", secondary=PostTags.__table__, back_populates="posts")
    
    def __repr__(self):
        author_email = self.author.email if self.author else "No author"
        return f"{self.title_en} (by {author_email})"


class Link(db.Model):
    __tablename__ = "link"
    
    id = db.Column(db.Integer, primary_key=True)
    
    alias = db.Column(db.String(100), unique=True, nullable=False, index=True)
    target = db.Column(db.String(2048), nullable=False)
    
class File(db.Model):
    __tablename__ = "file"
    
    id = db.Column(db.Integer, primary_key=True)
    
    uuid = db.Column(db.String(36), unique=True, nullable=False, index=True)
    
    name_en = db.Column(db.String(100), nullable=False)
    name_pl = db.Column(db.String(100), nullable=False)
    
    description_en = db.Column(db.Text())
    description_pl = db.Column(db.Text())
    
    category = db.Column(db.String(100), nullable=False)
    
    type = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(100), nullable=False)