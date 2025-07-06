#!/usr/bin/python3
""" holds class post_content"""

from .base_model import BaseModel
from . import db


class PostContent(BaseModel):
    """Representation of a post"""
    __tablename__ = 'post_content'
    
    post_id = db.Column('postid', db.String(60), db.ForeignKey('posts.id'), nullable=False)
    content = db.Column('content', db.String(65535))

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
