# Built-in imports
import os.path
from pathlib import Path

# Thirty part imports
from dotenv import load_dotenv
from flask import Flask
from flask_admin import Admin
from flask_babel import Babel
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy  # https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/

# Local imports
from config import app_config
from .models import db, Venta
from .utils.utils import build_sample_db

# from src.utils.utils import build_sample_db

# Load all environment variables from the .env file
load_dotenv()

# db = SQLAlchemy()

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
        # import secrets and generate a good keys using this library
        # Generate a nice key using secrets.token_urlsafe()
        SECRET_KEY=os.getenv("SECRET_KEY", "ThIsIsAdEfAuLtKeYiNcAsEnOtFoUnDInThEdOtEnV"),
        # Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
        # Generate a good salt using secrets.SystemRandom().getrandbits(128)
        SECURITY_PASSWORD_SALT=os.getenv("SECURITY_PASSWORD_SALT", "ThIsIsAdEfAuLtKeYiNcAsEnOtFoUnDInThEdOtEnV"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,  # avoid FSADeprecationWarning
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{Path(db_dir, 'suministros.db')}",
        UPLOAD_FOLDER=UPLOAD_FOLDER,
        # Have session and remember cookie be samesite (flask/flask_login)
        REMEMBER_COOKIE_SAMESITE="strict",
        SESSION_COOKIE_SAMESITE="strict",
    )
    # https://python-babel.github.io/flask-babel/
    # It is used for internationalization and localization support in Flask applications
    babel = Babel(app)

    # https://pythonhosted.org/Flask-Bootstrap/
    # Flask-Bootstrap packages Bootstrap into an extension that mostly consists of a blueprint named ‘bootstrap’.
    # It can also create links to serve Bootstrap from a CDN and works with no boilerplate code in your application.
    Bootstrap(app)

    db.init_app(app)

    if db_folder_created:
        with app.app_context():
            build_sample_db()

    # Some imports are being done here to avoid circular import issues
    from src.auth.views import login_manager

    login_manager.init_app(app)
    login_manager.login_message = "Debes iniciar sesión para acceder a esta página"
    login_manager.login_view = "auth.login"

    from src.admin.views import MyAdminIndexView, UsuarioModelView, ProductoModelView, VentaModelView

    admin = Admin(
        app,
        name="Maria Online Store",
        index_view=MyAdminIndexView(),
        base_template="my_master.html",
        template_mode="bootstrap4",
    )

    from .models import Usuario, Producto

    admin.add_view(UsuarioModelView(Usuario, db.session))
    admin.add_view(ProductoModelView(Producto, db.session))
    admin.add_view(VentaModelView(Venta, db.session))

    migrate = Migrate(app, db)  # https://flask-migrate.readthedocs.io/en/latest/

    # Admin Blueprint
    from .admin import admin as admin_bp  # rename to avoid circular import error

    app.register_blueprint(admin_bp, name="admin_bp")

    # Authorization Blueprint
    from .auth import auth

    app.register_blueprint(auth)

    # Home Blueprint
    from .home import home

    app.register_blueprint(home)

    # Product Blueprint
    from .producto import producto as producto_bp  # rename to avoid circular import error

    app.register_blueprint(producto_bp, name="producto_bp")

    # Store Blueprint
    from .store import store

    app.register_blueprint(store)

    # User Blueprint
    from .usuario import usuario

    app.register_blueprint(usuario)

    return app
