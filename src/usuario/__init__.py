from flask import Blueprint

usuario = Blueprint("usuario", __name__)

from . import views
