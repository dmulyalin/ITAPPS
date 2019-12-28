from flask import abort, flash, redirect, render_template, url_for, request
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
@login_required
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
            datum = dict(v.items())
            datum["id"] = v.identity
            devices.append(datum)
            
    return render_template('devices/devices.html', title="Devices", devices=devices)

@devices.route('/devices/add', methods=['GET', 'POST'])
@login_required
def add_device():
    """
    Add device to database
    """
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
    return render_template('devices/add_device.html', form=form,
                           title="Add Device")

@devices.route('/devices/delete/<int:id>', methods=['GET'])
@login_required
def delete_device(id):
    """
    Render the devices dashboard template on the /devices route
    """
    if graph is None or node_matcher is None:
        get_graph()
    graph.run("MATCH (n) WHERE ID(n)={} DETACH DELETE n".format(id))
    flash("Node deleted successfully")
    
    # redirect to devices page
    return redirect(url_for('devices.list_devices'))    

@devices.route('/devices/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_device(id):
    """
    Render the devices template for editing
    """
    if graph is None or node_matcher is None:
        get_graph()
    device_node = graph.evaluate("MATCH (n) WHERE ID(n)={} RETURN n".format(id))
    node_properties = dict(device_node.items())
    node_properties["id"] = id

    form = DeviceForm(**node_properties)
    if form.validate_on_submit():
        has_changes = False
        for k, v in form.data.items():
            if k in node_properties:
                if node_properties[k] != v:
                    device_node.update({k: v})
                    has_changes = True
            elif k not in ["id", "csrf_token"]:
                device_node.update({k: v})
                has_changes = True
        if has_changes:
            graph.push(device_node)

        # redirect to devices page
        return redirect(url_for('devices.list_devices'))
    
    return render_template('devices/edit_device.html', title="Edit Device", 
                           form=form)