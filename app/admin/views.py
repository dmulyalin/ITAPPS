from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import admin
from .forms import AddUserForm
from .. import db
from .. models import User


@admin.route('/users', methods=['GET', 'POST'])
@login_required
def list_users():
    """
    List all available users
    """
    pass

@admin.route('/users/delete', methods=['GET', 'POST'])
@login_required
def delete_user():
    pass


@admin.route('/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
    """
    Handle requests to add new user
    """
    pass
