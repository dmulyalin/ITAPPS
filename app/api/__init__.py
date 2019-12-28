"""
curl -X POST -u email:password http://192.168.64.128:9000/api/tokens  <- to get token
curl -X GET http://192.168.64.128:9000/api/devices -H "Authorization:Bearer token_goes_here" <- to get somthing with token auth
"""

from flask import Blueprint

api = Blueprint('api', __name__)

from . import devices, errors, tokens