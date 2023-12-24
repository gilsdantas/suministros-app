# Built-in imports
import os.path
from pathlib import Path

# Thirty part imports
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
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

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_message = "Debes iniciar sesión para acceder a esta página"
    login_manager.login_view = "auth.login"

    return app
