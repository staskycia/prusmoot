from flask import Flask

from config import Config

from app.extensions import db, login_manager, mail, admin, babel, get_locale

from app.admin_views import init_admin_views

from datetime import time, date
    
def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    login_manager.init_app(app)
    
    mail.init_app(app)
    
    admin.init_app(app)
    init_admin_views()
    
    babel.init_app(app, locale_selector=get_locale)
    
    #time and date constructors
    app.jinja_env.globals['time'] = time
    app.jinja_env.globals['date'] = date
    #get locale for jinja
    app.jinja_env.globals['get_locale'] = get_locale
    #getattr for jinja
    app.jinja_env.globals['getattr'] = getattr
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    
    from app.panel import bp as panel_bp
    app.register_blueprint(panel_bp, url_prefix="/panel")
    
    from app.link import bp as link_bp
    app.register_blueprint(link_bp, url_prefix="/link")
    
    return app