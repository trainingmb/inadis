#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Creator """
from models.creator import Creator
from models import db
from api.v1.views import api_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@api_views.route('/creators', methods=['GET'], strict_slashes=False)
#@swag_from('documentation/creator/all_creators.yml')
def get_creators():
    """
    Retrieves the list of all creator objects
    or a specific creator
    """
    all_creators = Creator.query.all()
    list_creators = []
    for creator in all_creators:
        list_creators.append(creator.to_dict())
    return jsonify(list_creators)


@api_views.route('/creators/<creator_id>', methods=['GET'], strict_slashes=False)
#@swag_from('documentation/creator/get_creator.yml', methods=['GET'])
def get_creator(creator_id):
    """
    Retrieves an creator
    """
    creator = Creator.query.get(creator_id)
    if not creator:
        abort(404, "Creator Not Found")

    return jsonify(creator.to_dict())


@api_views.route('/creators/<creator_id>', methods=['DELETE'],
                 strict_slashes=False)
#@swag_from('documentation/creator/delete_creator.yml', methods=['DELETE'])
def delete_creator(creator_id):
    """
    Deletes a creator Object
    """
    creator = Creator.query.get(creator_id)

    if not creator:
        abort(404)

    db.session.delete(creator)
    db.session.commit()

    return make_response(jsonify({}), 200)


@api_views.route('/creators', methods=['POST'], strict_slashes=False)
#@swag_from('documentation/creator/post_creator.yml', methods=['POST'])
def post_creator():
    """
    Creates a creator
    """
    crt = request.get_json()
    if not crt:
        abort(400, description="Not a JSON")
    for i, j in [('reference', int), ('name', str), ('link', str)]:
        if i not in crt:
            abort(400, description="Missing " + i)
        elif type(crt[i]) != j:
            abort(400, description="Type of {} is invalid required is {} ".format(i, j))

    data = request.get_json()
    instance = Creator(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@api_views.route('/creators/<creator_id>', methods=['PUT'], strict_slashes=False)
#@swag_from('documentation/creator/put_creator.yml', methods=['PUT'])
def put_creator(creator_id):
    """
    Updates a creator
    """
    creator = Creator.query.get(creator_id)

    if not creator:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(creator, key, value)
    creator.save()
    return make_response(jsonify(creator.to_dict()), 200)