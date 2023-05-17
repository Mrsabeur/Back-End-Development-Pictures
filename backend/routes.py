from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return data, 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    url = ""
    for pics in data:
        if pics["id"] == id:
            url = pics
    
    if url == "":
        return {"message": "Pic not found"}, 404
    else:
        return url, 200


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    pic = request.json
    
    for pics in data:
        if pics["id"] == pic["id"]:
            return {"Message": "picture with id {} already present".format(pic["id"])}, 302
    
    data.append(pic)
    return pic, 201
######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    update = request.json
    for i in range(len(data)):
        if data[i]["id"] == id:
            data[i] = update
            return data[i], 200
    
    return {"message": "picture not found"}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for i in range(len(data)):
        if data[i]["id"] == id:
            del(data[i])
            return "", 204
    
    return {"message": "picture not found"}, 404
