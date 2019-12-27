from flask import abort, render_template
from flask_login import current_user, login_required

from . import home


@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('base.html', title="ITAPPS")