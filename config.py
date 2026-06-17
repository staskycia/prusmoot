import os

basedir = os.path.abspath(os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

class Config:
    with open(os.path.join(basedir, "secret_key.txt")) as f:
        SECRET_KEY = f.read()
    SERVER_NAME = os.getenv("SERVER_NAME")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")
    UPLOAD_FOLDER = "uploaded_files"
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", "False").lower() == "true"
    BABEL_TRANSLATION_DIRECTORIES = os.getenv(
        "BABEL_TRANSLATION_DIRECTORIES",
        os.path.join(basedir, "translations")
    )