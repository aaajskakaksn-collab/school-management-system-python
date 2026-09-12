# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'الرجاء تسجيل الدخول للمتابعة.'


def create_app():
    app = Flask(__name__, static_folder='app/static', template_folder='app/templates')
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    # Import and register blueprints
    from app.auth import auth_bp
    from app.admin_views import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    return app
