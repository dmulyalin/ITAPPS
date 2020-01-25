from flask import abort, flash, redirect, render_template, url_for, request, send_from_directory
from flask_login import login_required, current_user

from . import devices

@devices.route('/devices/devices_table.html')
@login_required
def devices_table_view():
    # Render the devices table view template
    return render_template('devices/devices_table.html', title="Devices Table")

@devices.route('/devices/devices_3d.html')
@login_required
def devices_3d_view():
    # Render the devices 3D view template
    return render_template('devices/devices_3d.html', title="Devices 3D")

@devices.route('/devices/devices_3d.js')
@login_required
def devices_3d_view_js():
    # Render the devices 3D view template
    return send_from_directory('/root/ITAPPS-2/app/static/js', "devices_3d.js")

@devices.route('/devices/create.html', methods=['GET'])
@login_required
def add_device():
    # Return device create template structure
    return render_template('devices/create.html')

@devices.route('/devices/device.html')
@login_required
def device_location():
    # Supply the device template view on the /devices/device route
    return render_template('devices/device.html', title="device")

@devices.route('/devices/import.html')
@login_required
def device_import():
    # Supply the device template view on the /devices/device route
    return render_template('devices/import.html', title="device impot")