#!/usr/bin/python3
"""
Initialize Models Package
"""

from flask_sqlalchemy import SQLAlchemy

# Initialize Flask-SQLAlchemy
db = SQLAlchemy()

# Import models in dependency order to avoid circular imports
from .user import User
from .creator import Creator
from .creation import Creation
from .post import Post
from .post_content import PostContent
from .user_creation import UserCreation