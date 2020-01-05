from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import login_required, current_user

from . import locations

@locations.route('/locations')
@login_required
def locations():
    """
    Render the locations page view on the /locations route
    """           
    return render_template('locations/locations.html', title="locations")