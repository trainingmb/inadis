#!/usr/bin/python3
""" objects that handles all default RestFul API actions for posts """
from models.post import Post
from models.creator import Creator
from models.creation import Creation
from models.post_content import PostContent
from models import storage
from api.v2.views import api_views
from flask import abort, jsonify, make_response, request
from datetime import datetime
import dateutil.parser
from flasgger.utils import swag_from
from regex import match

post_tp = {'title': str, 'content': str, "comment": str,
           'reference': int, "posted_at": datetime, "fetched_at": datetime}
time = "%Y-%m-%dT%H:%M:%S.%f"

@api_views.route('/creators/<creator_id>/creations/<creation_id>/posts', methods=['GET'],
                 strict_slashes=False)
#@swag_from('documentation/post/posts_by_creation.yml', methods=['GET'])
def get_posts(creator_id, creation_id):
    """
    Retrieves the list of all posts objects
    of a specific Creation, or a specific post
    """
    list_posts = []
    creator = storage.get(Creator, creator_id)
    if not creator:
        abort(404, "Creator Not Found")
    creation = storage.get(Creation, creation_id)
    if not creation or creator.id != creation.creator_id:
        abort(404, "Creation Not Found")
    for post in creation.posts:
        list_posts.append(post.to_dict())
    return jsonify(list_posts)


@api_views.route('/posts/<post_id>/', methods=['GET'], strict_slashes=False)
#@swag_from('documentation/post/get_post.yml', methods=['GET'])
def get_post(post_id):
    """
    Retrieves a specific post based on id
    """
    post = storage.get(Post, post_id)
    if not post:
        abort(404, "Post Not Found")
    return jsonify(post.to_dict())


@api_views.route('/posts/<post_id>', methods=['DELETE'], strict_slashes=False)
#@swag_from('documentation/post/delete_post.yml', methods=['DELETE'])
def delete_post(post_id):
    """
    Deletes a post based on id provided
    """
    post = storage.get(Post, post_id)

    if not post:
        abort(404, "Post Not Found")
    storage.delete(post)
    storage.save()

    return make_response(jsonify({}), 200)


@api_views.route('/creators/<creator_id>/creations/<creation_id>/posts', methods=['POST'],
                 strict_slashes=False)
#@swag_from('documentation/post/post_post.yml', methods=['POST'])
def post_post(creator_id, creation_id):
    """
    Creates a Post
    """
    creator = storage.get(Creator, creator_id)
    if not creator:
        abort(404, "Creator Not Found")
    creation = storage.get(Creation, creation_id)
    if not creation or creator.id != creation.creator_id:
        abort(404, "Creation Not Found")
    crt = request.get_json()
    if not crt:
        abort(400, description="Not a JSON")
    for i, j in post_tp.items():
        if i not in crt:
            abort(400, description="Missing " + i)
        elif type(crt[i]) != j:
            abort(400, description="Type of {} is invalid required is {} ".format(i, j))

    data = request.get_json()
    instance = Post(**data)
    instance.creation_id = creation.id
    instance.save()
    instance2 = PostContent(post_id=instance.id, content=data.get('content', ''))
    instance2.save()
    return make_response(jsonify(instance.to_dict()), 201)

@api_views.route('/generate_post', methods=['POST'],
                 strict_slashes=False)
#@swag_from('documentation/post/gen_post.yml', methods=['POST'])
def gen_post():
    """
    Creates a Post
    """
    crt = request.get_json()
    if not crt:
        abort(400, description="Not a JSON")
    list_creations = []
    creator_reference = crt.get('url','').split('/')[-3]
    if not creator_reference.isnumeric():
        abort(400, "Creator Reference Invalid")
    all_creators = storage.all(Creator).values()
    creator = None
    for cr in all_creators:
        if cr.reference == int(creator_reference):
            creator = cr
            break
    if creator is None:
        abort(404, "Creator Not Found")
    creations = creator.creations
    if len(creations) < 1:
        abort(404, "Creator Does Not have Creations")
    for create in creations:
        #.encode('utf-8-sig').decode('unicode_escape')
        if match(create.regexfilter, crt.get('title',"")) is not None or match(create.regexfilter, crt.get('title',"")) is not None:
            data = {}
            data2 = {}
            data['title'] = crt.get('title',"")
            data2['content'] = crt.get('content',"")
            data['comment'] = crt.get('comment',"")
            data['reference'] = crt.get('url','').split('/')[-1]
            data['posted_at'] = crt.get('published',"")
            data['fetched_at'] = datetime.now()
            if data['reference'].isnumeric():
                data['reference'] = int(data['reference'])
            else:
                data['reference'] = 0
            if data['posted_at'] != "":
                p = data['posted_at']
                p = p.replace('Published: ','')
                p = p.replace(' ','T')
                p += '.00'
                try:
                    data['posted_at'] = dateutil.parser.parse(p)
                except Exception:
                    data['posted_at'] = datetime.now()
            else:
                data['posted_at'] = datetime.now()
            instance = Post(**data)
            instance.creation_id = create.id
            instance2 = PostContent(**data2)
            instance2.post_id = instance.id
            instance.save()
            instance2.save()
            # pts = {i.reference:i for i in create.posts_no_content}
            # if pts.get(data['reference'], None) is not None:
            #     storage.get(Post, pts.get(data['reference'], None).id).delete()
            return make_response(jsonify({"creationid": create.id, "creationname": create.name}), 201)
    return make_response(jsonify({"creationid": None, "creationname": ""}), 201)

@api_views.route('/posts/<post_id>', methods=['PUT'], strict_slashes=False)
#@swag_from('documentation/post/put_post.yml', methods=['PUT'])
def put_post(post_id):
    """
    Updates a Post
    """
    post = storage.get(Post, post_id)
    if not creation:
        abort(404, "Creation Not Found")

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    ignore = ['id', 'creation_id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            if key in post_tp.keys() and type(value) == post_tp[key]:
                setattr(post, key, value)
    storage.save()
    return make_response(jsonify(post.to_dict()), 200)