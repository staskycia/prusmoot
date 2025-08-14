from flask import render_template, url_for, request, redirect, current_app, send_file, abort

from app.main import bp

from app.extensions import db
from app.models import Post, Tag, File

@bp.route("/")
def home():
    return render_template("home.html")

@bp.route("/about")
def about():
    return render_template("about.html")

@bp.route("/edition/<int:year>")
def edition(year):
    return render_template(f"editions/{year}.html")

from pathlib import Path

@bp.route("/files")
def files():
    UPLOAD_DIR = (Path(current_app.root_path) / current_app.config["UPLOAD_FOLDER"]).resolve()
    
    path = (current_app.root_path/Path(current_app.config.get("UPLOAD_FOLDER"))/request.args.get("folder", "2025")).resolve(strict=False)
   
    if not path.exists() or not str(path).startswith(str(UPLOAD_DIR)):
        path = UPLOAD_DIR / "2025"
    
    files = list()
    
    for item in path.iterdir():
        if item.is_file():
            uuid = item.name.split('.')[0]
            file_data = File.query.filter_by(uuid=uuid).first_or_404()
            files.append((uuid, file_data.name_en, file_data.icon, file_data.description_en, file_data.type))
            
    return render_template("files.html", files=files, folder=request.args.get("folder", "2025"))

@bp.route("/download/<folder>/<file>")
def download(folder, file):
    UPLOAD_DIR = (Path(current_app.root_path) / current_app.config["UPLOAD_FOLDER"]).resolve()
    
    path = (current_app.root_path/Path(current_app.config.get("UPLOAD_FOLDER"))/folder/file).resolve(strict=False)
    
    if not path.exists() or not str(path).startswith(str(UPLOAD_DIR)):
        abort(404)
    
    return send_file(str(path))
    

@bp.route("/news")
def news():
    page = request.args.get("page", 1, type=int)
    per_page = 5
    
    tag_id = request.args.get("tag", None, type=int)
    
    query = Post.query.order_by(Post.created_at.desc())
    
    if tag_id:
        query = query.filter(Post.tags.any(Tag.id == tag_id))
        
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    # pagination = Post.query.order_by(Post.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template("news.html", posts=pagination.items, pagination=pagination, tag_id=tag_id)

@bp.route("/post/<int:id>")
def post(id):
    post = db.session.get(Post, id)
    
    if not post:
        return redirect(url_for("main.news"))
    
    return render_template("post.html", post=post)

@bp.route("/guide")
def guide():
    return "Guide will be here!"