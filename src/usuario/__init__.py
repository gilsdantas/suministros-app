from flask import Blueprint

usuario = Blueprint("usuario_bp", __name__)

from . import views
