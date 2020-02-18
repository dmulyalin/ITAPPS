import os
from flask import Flask, flash, request, redirect, url_for, jsonify, current_app

from . import api
from . import errors
from app.api.auth import token_auth

UPLOAD_FOLDER = os.path.join(current_app.config["BASEDIR"], 'app/upload_folder')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api.route('/api/misc/upload', methods=['GET', 'POST'])
#@token_auth.login_required
def upload():
    ret = {"Message": "", "Status": ""} 

    if request.method == 'POST':
        # check if the post request has the file part
        if "device_config_file" in request.files:
            file = request.files["device_config_file"]
            ret['Message'] = "Got config file {}".format(UPLOAD_FOLDER)
            return jsonify(ret)      
        
        file.save(os.path.join(UPLOAD_FOLDER, filename))
    
    return jsonify(ret)