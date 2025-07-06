#!/usr/bin/python3
"""
Index for V1 App
"""
from app.v1.views import app_views, jsonify, render_template
from models import db
from models.creator import Creator
from models.creation import Creation
from models.post import Post


@app_views.route('/home')
def home():
    """
    Home for the website
    """
    return render_template("user/home.html")


@app_views.route('/about')
def about():
    """
    Return the JSON statistics
    for all classes
    """
    cls = {'Creator': Creator.query.count(),
           'Creation': Creation.query.count(),
           'Posts': Post.query.count()}
    return render_template("user/about.html", cls=cls)