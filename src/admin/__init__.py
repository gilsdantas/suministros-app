from flask import Blueprint

admin = Blueprint("admin_bp", __name__)

from . import views
