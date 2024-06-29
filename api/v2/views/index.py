#!/usr/bin/python3
""" Index """
from models.creation import Creation
from models.creator import Creator
from models.post import Post
from models import storage
from api.v2.views import api_views
from flask import jsonify


@api_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Status of API """
    return jsonify({"status": "OK"})


@api_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_objects():
    """ Retrieves the number of each objects by type """
    classes = {"Creator": Creator, "Creation": Creation,
                "Post": Post}

    num_objs = {}
    for name, cl in classes.items():
        num_objs[name] = storage.count(cl)
    return jsonify(num_objs)