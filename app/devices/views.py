from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import login_required, current_user

from . import devices

@devices.route('/devices/devices.html')
@login_required
def list_devices():
    # Render the devices dashboard template
    return render_template('devices/devices.html', title="Devices")

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