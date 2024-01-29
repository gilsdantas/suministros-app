# Built-in imports
import os.path
from pathlib import Path

# Thirty part imports
from flask import Flask
from flask_admin import Admin
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy  # https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/

# Local imports
from config import app_config

db = SQLAlchemy()
# login_manager = LoginManager()  # https://flask-login.readthedocs.io/en/latest/

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
    db_folder_created = False
    # Create a 'database' folder if it is not done yet
    try:
        os.makedirs(Path(CURRENT_DIR, "database"))
        db_folder_created = True
    except OSError:
        pass

    db_dir = Path(CURRENT_DIR, "database")

    app.config.from_object(app_config[config_name])
    app.config.from_pyfile("config.py", silent=True)
    app.config.from_mapping(
        SECRET_KEY="TeMpOrArYkEyHaSbEeNuSeD",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,  # avoid FSADeprecationWarning
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{Path(db_dir, 'suministros.db')}",
        UPLOAD_FOLDER=UPLOAD_FOLDER,
    )

    # https://pythonhosted.org/Flask-Bootstrap/
    # Flask-Bootstrap packages Bootstrap into an extension that mostly consists of a blueprint named ‘bootstrap’.
    # It can also create links to serve Bootstrap from a CDN and works with no boilerplate code in your application.
    Bootstrap(app)

    db.init_app(app)

    if db_folder_created:
        from src.models import build_sample_db

        with app.app_context():
            build_sample_db()

    from src.auth.views import login_manager

    login_manager.init_app(app)
    login_manager.login_message = "Debes iniciar sesión para acceder a esta página"
    login_manager.login_view = "auth.login"

    from src.admin.views import MyAdminIndexView, MyAdminModelView

    admin = Admin(
        app,
        name="Maria Online Store",
        index_view=MyAdminIndexView(),
        # base_template='base.html',
        template_mode="bootstrap4",
    )
    from src.models import Usuario

    admin.add_view(MyAdminModelView(Usuario, db.session))

    migrate = Migrate(app, db)  # https://flask-migrate.readthedocs.io/en/latest/

    # Admin Blueprint
    from .admin import admin_bp

    app.register_blueprint(admin_bp)

    # Authorization Blueprint
    from .auth import auth

    app.register_blueprint(auth)

    # Home Blueprint
    from .home import home

    app.register_blueprint(home)

    # Product Blueprint
    from .producto import producto

    app.register_blueprint(producto)

    # Store Blueprint
    from .store import store

    app.register_blueprint(store)

    # User Blueprint
    from .usuario import usuario

    app.register_blueprint(usuario)

    return app
