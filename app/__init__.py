from flask import Flask

from config import Config

from app.extensions import db, login_manager, mail
    
def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    login_manager.init_app(app)
    
    mail.init_app(app)
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    return app