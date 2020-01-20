from flask import url_for, jsonify, request, g, abort, flash
from flask_login import login_required, current_user
from app.api.auth import token_auth
from py2neo import Graph, Node, Relationship, NodeMatcher

from . import api
from . import errors
from .structs import locations as loactions_struct

# initiate graph
graph = None
node_matcher = None
def get_graph():
    global graph
    global node_matcher
    graph = Graph(host="192.168.64.128", password="Kotr5rik", username="neo4j")
    node_matcher = NodeMatcher(graph)

@api.route('/api/locations', methods=['GET'])
@token_auth.login_required
def get_locations():
    """
    Return lists of locations
    """
    if graph is None:
        get_graph()
    # get page and per_page params from URL extract page and per_page from the query 
    # string of the request, using the defaults of 1 and 10 respectively if they are 
    # not defined. The per_page has additional logic that caps it at 100.
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    brief = request.args.get('brief', False, type=bool)
    
    # get locations from database
    locations = []
    if brief:
        locations_nodes = graph.run("MATCH (n:Location) RETURN n.name as name, n.description as description, ID(n) as id").data()
        locations = locations_nodes
    else:
        locations_nodes = graph.run("MATCH (n:Location) RETURN n").data()
        for location in locations_nodes:
            for k, v in location.items():
                datum = dict(v.items())
                datum["id"] = v.identity
                locations.append(datum)
    return jsonify({
        "data": locations,
        "meta": {
            "page": page,
            "per_page": per_page
        }
    })

@api.route('/api/locations/<int:id>', methods=['GET'])
@token_auth.login_required
def get_location(id):
    """
    Return location by id
    """
    if graph is None:
        get_graph()
    # get location from database
    location_node = graph.evaluate("MATCH (n) WHERE ID(n)={} RETURN n".format(id))
    if location_node:
        location_properties = dict(location_node.items())
        location_properties["id"] = id
        return jsonify({"data": location_properties})
    else:
        return errors.error_response(404, message="Location node with id '{}' not found in databse".format(id))
    
@api.route('/api/locations/create', methods=['POST'])
@token_auth.login_required
def create_location():
    data = request.get_json() or {}
    ret = {"Message": "", "Status": ""}
    if data:
        if graph is None:
            get_graph()
        # add location to gaph database
        location_node = Node(*(data["labels"]["mandatory"] + data["labels"]["optional"]))
        # add mandatory properties
        for property in data["properties"]["mandatory"]:
            if not property["propertyName"] in location_node:
                location_node.update({property["propertyName"]: property["propertyValue"]})
        # add optional properties
        for property in data["properties"]["optional"]:
            if not property["propertyName"] in location_node:
                location_node.update({property["propertyName"]: property["propertyValue"]})  
        # add location to graph
        graph.merge(location_node, "Location", "name")
        ret["Message"] = "location created successfully: {}".format(location_node["name"])
    return jsonify(ret)
    
@api.route('/api/locations/templates', methods=['GET'])
@token_auth.login_required
def get_location_create_form():
    return jsonify(loactions_struct.nodes["location_node_base"])

@api.route('/api/locations/delete', methods=['POST'])
@token_auth.login_required
def delete_location():
    data = request.get_json() or {}
    ret = {"Message": "", "Status": ""}
    if data:
        if graph is None:
            get_graph()
        # delete location(s) from gaph database
        for item in data:
            graph.evaluate("MATCH (n) WHERE ID(n)={} DETACH DELETE n".format(item["id"]))
            ret["Status"] += "Deleted location: {}\n".format(item["name"])
    return jsonify(ret)