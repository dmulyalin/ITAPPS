import os
from flask import Flask, flash, request, redirect, url_for, jsonify

from . import api
from . import errors
from app.api.auth import token_auth
from app import app

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api.route('/api/misc/upload', methods=['GET', 'POST'])
@token_auth.login_required
def upload():
    UPLOAD_FOLDER = os.path.join(app.config["BASEDIR"], 'app/upload_folder')
    ALLOWED_EXTENSIONS = [".txt", ".conf"]
    ret = {"Message": "", "Status": ""} 

    if request.method == 'POST':
        FILE_VERIFIFED = False
        # check if the post request has device_config_file file
        if "device_config_file" in request.files:
            file = request.files["device_config_file"]
            filename = file.filename
            extension = ".{}".format(filename.split(".")[-1].strip())
            if extension in ALLOWED_EXTENSIONS:
                FILE_VERIFIFED = True
            else:
                ret["Message"] = "device_config_file must have .txt extension, filename: {}".format(filename)
            UPLOAD_FOLDER = os.path.join(UPLOAD_FOLDER, 'device_configurations')
        else:
            ret["Message"] = "Not supported file context"
        
        if FILE_VERIFIFED:
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            ret["Message"] = "File: {}; Path: {}; Saved: {}".format(filename, UPLOAD_FOLDER, True)
    
    return jsonify(ret)

@api.route('/api/misc/ttp_templates', methods=['GET', 'POST'])
@token_auth.login_required
def ttp_templates():
    UPLOAD_FOLDER = os.path.join(app.config["BASEDIR"], 'app/upload_folder/ttp_templates')
    ALLOWED_EXTENSIONS = [".txt"]
    ret = {"Message": "", "Status": "", "ttp_templates": []} 

    if request.method == 'POST':
        FILE_VERIFIFED = False
        # check if the post request has device_config_file file
        file = request.files["ttp_template_files"]
        filename = file.filename
        extension = ".{}".format(filename.split(".")[-1].strip())
        if extension in ALLOWED_EXTENSIONS:
            FILE_VERIFIFED = True
        else:
            ret["Message"] = "TTP template must have .txt extension, filename: {}".format(filename)
        if FILE_VERIFIFED:
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            ret["Message"] = "File: {}; Path: {}; Saved: {}".format(filename, UPLOAD_FOLDER, True)
    elif request.method == 'GET':
        template_name = request.args.get('template_name', "_list_all_", type=str)
        if template_name == "_list_all_":
            ttp_templates_filenames = [f for f in os.listdir(UPLOAD_FOLDER)
                                       if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))]
            ret["ttp_templates"] = ttp_templates_filenames
        elif template_name.endswith(".txt"):
            with open(os.path.join(UPLOAD_FOLDER, template_name)) as file:
                ret["ttp_templates"][0] = file.read()

    return jsonify(ret)