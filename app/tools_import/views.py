from flask import abort, flash, redirect, render_template, url_for
from flask_login import login_required, current_user
from py2neo import Graph, Node, Relationship, NodeMatcher

from . import tools_import
from .forms import SampleForm

# initiate graph
graph = None
node_matcher = None
def get_graph():
    global graph
    global node_matcher
    graph = Graph(host="192.168.64.128", password="Kotr5rik", username="neo4j")
    node_matcher = NodeMatcher(graph)

@tools_import.route('/tools/import')
# @login_required
def tools_import():
    """
    Render the tools_import template 
    """
    return render_template('tools/import.html', title="Import")