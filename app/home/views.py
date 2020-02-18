from flask import abort, render_template
from flask_login import current_user, login_required

from . import home


@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('base.html', title="ITAPPS")

@home.route('/front_page.html')
def frontpage():
    """
    Render the frontpage template
    """
    return render_template('front_page/front_page.html', title="Home")