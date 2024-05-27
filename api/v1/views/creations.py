#!/usr/bin/python3
""" objects that handles all default RestFul API actions for creations """
from models.creation import Creation
from models.creator import Creator
from models import storage
from api.v1.views import api_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from

creation_tp = {'regexfilter': str, 'name': str}

@api_views.route('/creations', methods=['GET'],
                 strict_slashes=False)
#@swag_from('documentation/creation/creations_by_creator.yml', methods=['GET'])
def get_all_creations():
    """
    Retrieves the list of all creations objects
    """
    list_creations = [i.to_dict() for i in storage.all(Creation).values()]
    return jsonify(list_creations)

@api_views.route('/creators/<creator_id>/creations', methods=['GET'],
                 strict_slashes=False)
#@swag_from('documentation/creation/creations_by_creator.yml', methods=['GET'])
def get_creations(creator_id):
    """
    Retrieves the list of all creations objects
    of a specific Creator, or a specific creation
    """
    list_creations = []
    creator = storage.get(Creator, creator_id)
    if not creator:
        abort(404, "Creator Not Found")
    for creation in creator.creations:
        list_creations.append(creation.to_dict())

    return jsonify(list_creations)

@api_views.route('/creators_reference/<creator_reference>/creations', methods=['GET'],
                 strict_slashes=False)
#@swag_from('documentation/creation/creations_by_creator_reference.yml', methods=['GET'])
def get_creations_by_reference(creator_reference):
    """
    Retrieves the list of all creations objects
    of a specific Creator, or a specific creation
    """
    list_creations = []
    if not creator_reference.isnumeric():
        abort(400, "Creator Reference Invalid")
    all_creators = storage.all(Creator).values()
    creator = None
    for cr in all_creators:
        if cr.reference == int(creator_reference):
            creator = cr
            break
    if not creator:
        abort(404, "Creator Not Found")
    for creation in creator.creations:
        list_creations.append(creation.to_dict())
    return jsonify(list_creations)

@api_views.route('/creations/<creation_id>/', methods=['GET'], strict_slashes=False)
#@swag_from('documentation/creation/get_creation.yml', methods=['GET'])
def get_creation(creation_id):
    """
    Retrieves a specific creation based on id
    """
    creation = storage.get(Creation, creation_id)
    if not creation:
        abort(404, "Creation Not Found")
    return jsonify(creation.to_dict())


@api_views.route('/creations/<creation_id>', methods=['DELETE'], strict_slashes=False)
#@swag_from('documentation/creation/delete_creation.yml', methods=['DELETE'])
def delete_creation(creation_id):
    """
    Deletes a creation based on id provided
    """
    creation = storage.get(Creation, creation_id)

    if not creation:
        abort(404, "Creation Not Found")
    storage.delete(creation)
    storage.save()

    return make_response(jsonify({}), 200)


@api_views.route('/creators/<creator_id>/creations', methods=['POST'],
                 strict_slashes=False)
#@swag_from('documentation/creation/post_creation.yml', methods=['POST'])
def post_creation(creator_id):
    """
    Creates a Creation
    """
    creator = storage.get(Creator, creator_id)
    if not creator:
        abort(404, "Creator Not Found")
    crt = request.get_json()
    if not crt:
        abort(400, description="Not a JSON")
    for i, j in creation_tp.items():
        if i not in crt:
            abort(400, description="Missing " + i)
        elif type(crt[i]) != j:
            abort(400, description="Type of {} is invalid required is {} ".format(i, j))

    data = request.get_json()
    instance = Creation(**data)
    instance.creator_id = creator.id
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)

@api_views.route('/creators_reference/<creator_reference>/creations', methods=['POST'],
                 strict_slashes=False)
#@swag_from('documentation/creation/creations_by_creator_reference_POST.yml', methods=['POST'])
def post_creations_by_reference(creator_reference):
    """
    Creates a Creation
    """
    list_creations = []
    if not creator_reference.isnumeric():
        abort(400, "Creator Reference Invalid")
    all_creators = storage.all(Creator).values()
    creator = None
    for cr in all_creators:
        if cr.reference == int(creator_reference):
            creator = cr
            break
    if not creator:
        abort(404, "Creator Not Found")
    crt = request.get_json()
    if not crt:
        abort(400, description="Not a JSON")
    for i, j in creation_tp.items():
        if i not in crt:
            abort(400, description="Missing " + i)
        elif type(crt[i]) != j:
            abort(400, description="Type of {} is invalid required is {} ".format(i, j))

    data = request.get_json()
    instance = Creation(**data)
    instance.creator_id = creator.id
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)

@api_views.route('/creations/<creation_id>', methods=['PUT'], strict_slashes=False)
#@swag_from('documentation/creation/put_creation.yml', methods=['PUT'])
def put_creation(creation_id):
    """
    Updates a Creation
    """
    creation = storage.get(Creation, creation_id)
    if not creation:
        abort(404, "Creation Not Found")

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    ignore = ['id', 'creator_id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            if key in creation_tp.keys() and type(value) == creation_tp[key]:
                setattr(creation, key, value)
    storage.save()
    return make_response(jsonify(creation.to_dict()), 200)