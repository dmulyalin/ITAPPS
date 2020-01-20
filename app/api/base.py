from flask import url_for, jsonify, request, g, abort, flash
from flask_login import login_required, current_user
from app.api.auth import token_auth

from . import api
from . import errors
from .structs import menu as menu_structs

@api.route('/api/misc/base_menu', methods=['GET'])
@token_auth.login_required
def get_base_menu_data():
    return jsonify(menu_structs.main)