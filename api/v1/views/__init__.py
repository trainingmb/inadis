#!/usr/bin/python3
""" Blueprint for API """
from flask import Blueprint

api_views = Blueprint('api_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.creators import *
from api.v1.views.creations import *
from api.v1.views.posts import *