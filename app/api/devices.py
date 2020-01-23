from flask import url_for, jsonify, request, g, abort
from flask_login import login_required, current_user
from app.api.auth import token_auth
from py2neo import Graph, Node, Relationship, NodeMatcher

from . import api
from . import errors
from .structs import devices as devices_struct

# initiate graph
graph = None
node_matcher = None
def get_graph():
    global graph
    global node_matcher
    graph = Graph(host="192.168.64.128", password="Kotr5rik", username="neo4j")
    node_matcher = NodeMatcher(graph)

@api.route('/api/devices', methods=['GET'])
@token_auth.login_required
def get_devices():
    """
    Return lists of devices
    """
    if graph is None:
        get_graph()
    # get page and per_page params from URL extract page and per_page from the query 
    # string of the request, using the defaults of 1 and 10 respectively if they are 
    # not defined. The per_page has additional logic that caps it at 100.
    page = request.args.get('page', 1, type=int)
    rows_per_page = min(request.args.get('rows_per_page', 30, type=int), 100)
    brief = request.args.get('brief', False, type=bool)
    order_by = request.args.get('order_by', "id", type=str)
    
    # get Devices from database
    devices = []
    skip = rows_per_page * (page - 1)
    query_count = "MATCH (n:Device) RETURN count(n)"
    query_brief = """
        MATCH (n:Device) 
        RETURN n.hostname as hostname, n.description as description, ID(n) as id
        ORDER BY n.{order_by}
        SKIP {skip} 
        LIMIT {limit}
    """
    query_details = "MATCH (n:Device) RETURN n"
    if brief:
        devices_nodes = graph.run(query_brief.format(order_by=order_by, skip=skip, limit=rows_per_page)).data()
        devices = devices_nodes
    else:
        devices_nodes = graph.run(query_details).data()
        for device in devices_nodes:
            for k, v in device.items():
                datum = dict(v.items())
                datum["id"] = v.identity
                devices.append(datum)
                
    # get overall device nodes and pages count
    overall = graph.run(query_count).data()[0]["count(n)"]
    pages = overall // rows_per_page + bool(overall % rows_per_page)
    
    # return results
    return jsonify({
        "data": devices,
        "meta": {
            "page": page,
            "rows_per_page": rows_per_page,
            "overall": overall,
            "order_by": order_by,
            "pages": list(range(1, pages+1))
        }
    })

@api.route('/api/devices/<int:id>', methods=['GET'])
@token_auth.login_required
def get_device(id):
    """
    Return device by id
    """
    if graph is None:
        get_graph()
    # get device from database
    device_node = graph.evaluate("MATCH (n) WHERE ID(n)={} RETURN n".format(id))
    if device_node:
        device_properties = dict(device_node.items())
        device_properties["id"] = id
        return jsonify({"data": device_properties})
    else:
        return errors.error_response(404, message="Device node with id '{}' not found in databse".format(id))
    
@api.route('/api/devices/templates', methods=['GET'])
@token_auth.login_required
def get_device_create_form():
    template_name = request.args.get('template_name', "base", type=str)
    if template_name == "_list_all_":
        return jsonify(list(devices_struct.nodes.keys()))
    return jsonify(devices_struct.nodes[template_name])

@api.route('/api/devices/create', methods=['POST'])
@token_auth.login_required
def create_device():
    data = request.get_json() or {}
    ret = {"Message": "", "Status": ""}
    if data:
        if graph is None:
            get_graph()
        # add device to gaph database
        device_node = Node(*(data["labels"]["mandatory"] + data["labels"]["optional"]))
        # add mandatory properties
        for property in data["properties"]["mandatory"]:
            if not property["propertyName"] in device_node:
                device_node.update({property["propertyName"]: property["propertyValue"]})
        # add optional properties
        for property in data["properties"]["optional"]:
            if not property["propertyName"] in device_node:
                device_node.update({property["propertyName"]: property["propertyValue"]})  
        # add device to graph
        graph.merge(device_node, "Device", "hostname")
        ret["Message"] = "device created successfully: {}".format(device_node["hostname"])
    return jsonify(ret)

@api.route('/api/devices/delete', methods=['POST'])
@token_auth.login_required
def delete_device():
    data = request.get_json() or {}
    ret = {"Message": "", "Status": ""}
    if data:
        if graph is None:
            get_graph()
        # delete Device(s) from gaph database
        for item in data:
            graph.evaluate("MATCH (n) WHERE ID(n)={} DETACH DELETE n".format(item["id"]))
            ret["Status"] += "Deleted device: {}\n".format(item["name"])
    return jsonify(ret)

@api.route('/api/devices/import', methods=['POST'])
@token_auth.login_required
def import_devices():
    data = request.get_json() or {}
    ret = {"Message": "", "Status": "OK"}
    if data:
        if graph is None:
            get_graph()
        # add devices' nodes to Graph Database
        if data["csv"]["nodes"]:
            nodes = []
            headers = []
            for row in iter(data["csv"]["nodes"].splitlines()):
                if not row.strip(): # skip empty rows
                    continue
                if not headers: # get headers
                    headers = [i.strip() for i in row.split(",") if i.strip()]
                    continue
                # make nodes dictionaries
                nodes.append({headers[index]: i for index, i in enumerate(row.split(",")) if i.strip()})
            for node in nodes:
                # check mandatory properties
                if not "hostname" in node:
                    continue
                # get labels
                labels = ["Device"]
                if "labels" in node:
                    labels += [i.strip() for i in node.pop("labels").split(";") if i.strip()]
                # add device to graph database
                device_node = Node(*labels, **node)
                # add device to graph
                graph.merge(device_node, "Device", "hostname")
                ret["Message"] += "device created successfully: {}; ".format(node["hostname"])
    return jsonify(ret)