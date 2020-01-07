from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import login_required, current_user

from . import locations

@locations.route('/locations')
@login_required
def locations_main_page():
    """
    Render the locations main page view on the /locations route
    """           
    return render_template('locations/locations.html', title="locations")

@locations.route('/locations/list.html')
@login_required
def list_locations():
    """
    Supply the locations list template view on the /locations/list route
    """           
    return render_template('locations/list.html', title="locations")

@locations.route('/locations/location.html')
@login_required
def list_location():
    """
    Supply the location template view on the /locations/location route
    """           
    return render_template('locations/location.html', title="location")

@locations.route('/locations/create.html')
@login_required
def create_location():
    """
    Supply the location create view on the /locations/create.html route
    """           
    return render_template('locations/create.html', title="location")