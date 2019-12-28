from flask import Blueprint

tools_import = Blueprint('tools_import', __name__)

from . import views
