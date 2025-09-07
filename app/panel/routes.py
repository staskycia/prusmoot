from flask import render_template, url_for, request, get_flashed_messages, flash, redirect, current_app
from app.panel import bp
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from app.extensions import db
from app.models import User, Link, Post, Tag, File

import re
from validators import url as is_valid_url

@bp.route("/", methods=["POST", "GET"])
@bp.route("/links", methods=["POST", "GET"])
@login_required
def home():
    links = Link.query.all()
    if request.method == "POST":
        field = request.form.get("field")
        if field == "add":
            alias = request.form.get("alias")
            target = request.form.get("target")
            if not (alias and target):
                flash("Both fields are required!", "error")
                return render_template("panel/links.html", links=links)
            if re.match(r"^[A-Za-z0-9_-]+$", alias) is None:
                flash("Alias can only include letters numbers and $ _ - + ! ( * ) symbols", "error")
                return render_template("panel/links.html", links=links)
            if not is_valid_url(target):
                flash("Invalid target URL! Make sure you start with https:// or http://", "error")
                return render_template("panel/links.html", links=links)
            if Link.query.filter_by(alias=alias).first():
                flash("Alias already in use!", "error")
                return render_template("panel/links.html", links=links)
            link = Link(alias=alias, target=target)
            db.session.add(link)
            db.session.commit()
            links = Link.query.all()
            flash("Link added!", "success")
        elif field == "delete":
            alias = request.form.get("alias")
            if not alias:
                flash("Link not found!", "error")
            else:
                link = Link.query.filter_by(alias = alias).first()
                if not link:
                    flash("Link not found!", "error")
                else:
                    db.session.delete(link)
                    db.session.commit()
                    flash("Link deleted!", "success")
                    links = Link.query.all()
            return render_template("panel/links.html", links=links)
                    
                
    return render_template("panel/links.html", links=links)

from bs4 import BeautifulSoup

def generate_samlpe(content):
    if len(content) > 1000:
        content = content[:1000]
    
    soup = BeautifulSoup(content, "lxml")
    
    for a in soup.find_all("a"):
        a.decompose()
    
    sample = soup.get_text()
    
    if len(sample) > 700:
        sample = sample[:700]
        
    return sample

@bp.route("/posts", methods=["POST", "GET"])
@login_required
def posts():
    tags = Tag.query.all()
    
    if request.method == "POST":
        title_en = request.form.get("title_en")
        title_pl = request.form.get("title_pl")
        
        content_en = request.form.get("content_en")
        content_pl = request.form.get("content_pl")
        
        if not (title_en and title_pl and content_en and content_pl):
            flash("All fields are required!", "error")
            return render_template("panel/posts.html", tags=tags, posts=posts)
        
        new_tags = request.form.getlist("tag_checkbox")
        
        post = Post(title_pl=title_pl, title_en=title_en, content_en=content_en, content_pl=content_pl, sample_en=generate_samlpe(content_en), sample_pl=generate_samlpe(content_pl), author_id=current_user.id, author=current_user)
        
        for tag in new_tags:
            post.tags.append(db.session.get(Tag, tag))
        
        db.session.add(post)
        db.session.commit()
        
        flash("Post publushed!", "success")
    
    posts = Post.query.order_by(Post.created_at.desc()).all()        
    return render_template("panel/posts.html", tags=tags, posts=posts)

@bp.route("/posts/edit/<id>", methods=["POST", "GET"])
@login_required
def edit_post(id):
    post = db.session.get(Post, id)
    
    if not post:
        return redirect(url_for("panel.posts"))
    
    tags = Tag.query.all()
    
    if request.method == "POST":
        post.title_en = request.form.get("title_en")
        post.title_pl = request.form.get("title_pl")
        
        post.content_en = request.form.get("content_en")
        post.content_pl = request.form.get("content_pl")
        
        post.sample_en = generate_samlpe(post.content_en)
        post.sample_pl = generate_samlpe(post.content_pl)
        
        new_tags = request.form.getlist("tag_checkbox")
        
        for tag in tags:
            if tag in post.tags and not str(tag.id) in new_tags:
                post.tags.remove(tag)
            elif not tag in post.tags and str(tag.id) in new_tags:
                post.tags.append(tag)
        
        
        db.session.commit()

        flash("Changes published!", "success")
        return redirect(url_for("panel.posts"))
    
    return render_template("panel/edit_post.html", post=post, tags=tags)

@bp.route("/posts/delete", methods=["POST"])
@login_required
def delete_post():
    id = request.form.get("id")
    
    if id:
        post = db.session.get(Post, id)
        
        if post:
            db.session.delete(post)
            db.session.commit()
            
            flash("Post deleted!", "success")
    
    return redirect(url_for("panel.posts"))

@bp.route("/tags", methods=["GET", "POST"])
@login_required
def tags():
    if request.method == "POST":
        name_en = request.form.get("name_en")
        name_pl = request.form.get("name_pl")
        color = request.form.get("color")
        if name_en and name_pl and color:
            tag = Tag(name_en=name_en, name_pl=name_pl, color=color)
            db.session.add(tag)
            db.session.commit()
            flash("Tag added!", "success")
        else:
            flash("All fields are required!", "error")
            
    tags = Tag.query.all()
    return render_template("panel/tags.html", tags=tags)

@bp.route("/tags/delete", methods=["POST"])
@login_required
def delete_tag():
    id = request.form.get("id")
    
    if id:
        tag = db.session.get(Tag, id)
        
        if tag:
            db.session.delete(tag)
            db.session.commit()
            
            flash("Tag deleted!", "success")
    
    return redirect(url_for("panel.tags"))

from pathlib import Path
from uuid import uuid4

@bp.route("/files", methods=["POST", "GET"])
@login_required
def files():
    categories = list()
    
    path = (current_app.root_path/Path(current_app.config.get("UPLOAD_FOLDER"))).resolve()
    
    for item in path.iterdir():
        if not item.is_file():
            categories.append(item.name)
    
    if request.method == "POST":
        name_en = request.form.get("name_en")
        name_pl = request.form.get("name_pl")
        
        description_en = request.form.get("description_en")
        description_pl = request.form.get("description_pl")
        
        category = request.form.get("category")
        
        if not name_en or not name_pl or not description_en or not description_pl or not "file" in request.files or not category or request.files["file"].filename == "":
            flash("All fields are required!", "error")
            return render_template("panel/files.html", categories=categories)
            
        file = request.files["file"]
        
        uuid = str(uuid4().hex)
        
        filetype = file.filename.split(".")[-1]
        
        filename = f"{uuid}.{filetype}"
        
        file.save((path/category/filename).resolve())
        
        icon = f"{filetype}.svg"
        
        icon_path = Path(Path(current_app.root_path)/"static"/"file_icons"/icon).resolve()
        
        if not icon_path.exists():
            icon = "blank.svg"
        
        db.session.add(File(uuid=uuid, name_en=name_en, name_pl=name_pl, description_en=description_en, description_pl=description_pl, type=filetype, icon=icon, category=category))
        db.session.commit()
        
        flash("File uploaded!", "success")
        
    files = File.query.all()
    return render_template("panel/files.html", categories=categories, files=files)

@bp.route("/files/delete", methods=["POST"])
@login_required
def delete_file():
    id = request.form.get("id")
    path = (current_app.root_path/Path(current_app.config.get("UPLOAD_FOLDER"))).resolve()
    
    if id:
        file = db.session.get(File, id)
        
        if file:
            category = file.category
            filename = f"{file.uuid}.{file.type}"
            
            file_path = Path((path/category/filename))
            
            file_path.unlink()
            
            db.session.delete(file)
            db.session.commit()
            
            flash("File deleted!", "success")
    
    return redirect(url_for("panel.files"))

@bp.route("/inactive")
@login_required
def inactive():
    flash("Sorry, your account isn't active!", "error")
    return render_template("panel/inactive.html")

@bp.before_request
def check_if_active():
    if current_user.is_authenticated and current_user.active and request.endpoint == "panel.inactive":
        return redirect(url_for("panel.home"))
    if current_user.is_authenticated and not current_user.active and not request.endpoint == "panel.inactive":
        return redirect(url_for("panel.inactive"))
    
@bp.before_request
def check_for_password_change():
    if current_user.is_authenticated and current_user.force_password_change and not request.endpoint == "auth.password_change":
        return redirect(url_for("auth.password_change"))