from flask import Blueprint

producto = Blueprint("producto", __name__)

from . import views
