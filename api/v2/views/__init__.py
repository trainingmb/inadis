#!/usr/bin/python3
""" Blueprint for API """
from flask import Blueprint

api_views = Blueprint('api_views', __name__, url_prefix='/api/v2')

from api.v2.views.index import *
from api.v2.views.creators import *
from api.v2.views.creations import *
from api.v2.views.posts import *