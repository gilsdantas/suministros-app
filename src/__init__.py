# Built-in imports
import os.path
from pathlib import Path

# Thirty part imports
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy  # https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/
from flask_login import LoginManager

# Local imports
from src import database
from config import app_config

db = SQLAlchemy()
login_manager = LoginManager()  # https://flask-login.readthedocs.io/en/latest/

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "svg", "gif", "bmp"}
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = "src/static"


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def create_app(config_name):
    """
    This is the application factory function. It creates and configures the app
    """

    app = Flask(__name__, instance_relative_config=True)

    try:
        os.makedirs(Path(CURRENT_DIR, "database"))
    except OSError:
        pass

    db_dir = Path(CURRENT_DIR, "database")

    app.config.from_object(app_config[config_name])
    app.config.from_pyfile("config.py", silent=True)
    app.config.from_mapping(
        SECRET_KEY="TeMpOrArYkEyHaSbEeNuSeD",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,  # avoid FSADeprecationWarning
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{Path(db_dir, 'producto.db')}",
        UPLOAD_FOLDER=UPLOAD_FOLDER,
    )

    # https://pythonhosted.org/Flask-Bootstrap/
    # Flask-Bootstrap packages Bootstrap into an extension that mostly consists of a blueprint named ‘bootstrap’.
    # It can also create links to serve Bootstrap from a CDN and works with no boilerplate code in your application.
    Bootstrap(app)

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_message = "Debes iniciar sesión para acceder a esta página"
    login_manager.login_view = "auth.login"

    migrate = Migrate(app, db)  # https://flask-migrate.readthedocs.io/en/latest/

    # Home Blueprint
    from .home import home as home_bprint

    app.register_blueprint(home_bprint)

    # Product Blueprint
    from .producto import producto as producto_bprint

    app.register_blueprint(producto_bprint)

    # Admin Blueprint
    from .admin import admin as admin_bprint

    app.register_blueprint(admin_bprint)

    # User Blueprint
    from .usuario import usuario as usuario_bprint

    app.register_blueprint(usuario_bprint)

    # Authorization Blueprint
    from .auth import auth as auth_bprint

    app.register_blueprint(auth_bprint)

    return app
