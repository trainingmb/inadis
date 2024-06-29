#!/usr/bin/python3
"""
Index for V1 App
"""
from app.v2.views import app_views, jsonify, render_template
from models import storage
from models.base_model import BaseModel, Base
from models.creator import Creator
from models.creation import Creation
from models.post import Post
from models.post_content import PostContent
from models.user import User

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
    cls = {'Creator': storage.count(Creator),
           'Creation': storage.count(Creation),
           'Posts': storage.count(Post),
           'Post Content': storage.count(PostContent),
           'User': storage.count(User)}
    return render_template("user/about.html", cls=cls)