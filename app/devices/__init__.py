from flask import Blueprint

devices = Blueprint('devices', __name__)

from . import views
