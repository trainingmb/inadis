#!/usr/bin/python3
"""
Init for Views in V2
"""
from flask import Blueprint, jsonify, abort, flash, redirect, request, render_template, url_for


app_views = Blueprint('app_views', __name__, url_prefix="/app/v2")

from app.v2.forms import *

from app.v2.views.auth import *
from app.v2.views.index import *
from app.v2.views.creators import *
from app.v2.views.creations import *
from app.v2.views.posts import *
from app.v2.views.users import *