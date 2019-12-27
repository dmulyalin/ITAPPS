from flask import abort, flash, redirect, render_template, url_for
from flask_login import login_required, current_user
from py2neo import Graph, Node, Relationship, NodeMatcher

from . import devices
from .forms import DeviceForm

# initiate graph
graph = None
node_matcher = None
def get_graph():
    global graph
    global node_matcher
    graph = Graph(host="192.168.64.128", password="Kotr5rik", username="neo4j")
    node_matcher = NodeMatcher(graph)

@devices.route('/devices')
# @login_required
def list_devices():
    """
    Render the devices dashboard template on the /devices route
    """
    if graph is None:
        get_graph()
    # get devices from database
    devices = []
    devices_nodes = graph.run("MATCH (n:Device) RETURN n").data()
    for device in devices_nodes:
        for k, v in device.items():
            devices.append(dict(v.items()))
            
    return render_template('devices/devices.html', title="Devices", devices=devices)

@devices.route('/devices/add', methods=['GET', 'POST'])
# @login_required
def add_device():
    """
    Add device to database
    """
    add_device = True

    form = DeviceForm()
    if form.validate_on_submit():
        if graph is None:
            get_graph()
        # add device to gaph database
        device_hostname = form.data['hostname']
        device_details = {
            'description': form.data['description'],
            'make': form.data.get('make', ''),
            'hardware': form.data.get('hardware', '')
        }
        device_node = Node('Device', hostname=device_hostname, **device_details)
        graph.merge(device_node, "Device", "hostname")
        flash('Device added successfully')
        # redirect to devices page
        return redirect(url_for('devices.list_devices'))

    # load device template
    return render_template('devices/add_device.html', action="Add",
                           add_device=add_device, form=form,
                           title="Add Device")

@devices.route('/devices/delete')
# @login_required
def delete_device():
    """
    Render the devices dashboard template on the /devices route
    """
    pass
    # return render_template('devices/add_device.html', title="Add Device")

@devices.route('/devices/edit')
# @login_required
def edit_device():
    """
    Render the devices template for editing
    """
    pass
    # return render_template('devices/edit.html', title="Edit Device")
    
@devices.route('/devices/edit')
# @login_required
def add_device_template():
    """
    Render the devices template for editing
    """
    pass
    # return render_template('devices/edit.html', title="Edit Device")