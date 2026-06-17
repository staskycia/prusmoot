import os
import secrets

key_path = os.path.abspath(os.path.join(__file__, "..", "secret_key.txt"))
os.makedirs(os.path.dirname(key_path), exist_ok=True)

if not os.path.exists(key_path):
    key = secrets.token_urlsafe(64)
    with open(key_path, "w") as f:
        f.write(key)
        
from app import create_app
app = create_app()

from app.extensions import db

from app.models import User, Post

from werkzeug.security import generate_password_hash

admin_email = input("Admin email: ")
admin_password = input("Admin password: ")

with app.app_context():
    db.create_all()

    existing = User.query.filter_by(email=admin_email).first()
    if existing is None:
        admin = User(email=admin_email, first_name="Staś", last_name="Kycia", password=admin_password, is_admin=True)
        db.session.add(admin)
        db.session.commit()
    else:
        print(f"Admin user already exists: {existing.email}")