#!/usr/bin/python3
""" holds class Post"""

from datetime import datetime
from .base_model import BaseModel
from . import db


class Post(BaseModel):
    """Representation of a post"""
    __tablename__ = 'posts'
    
    creation_id = db.Column('creationid', db.String(60), db.ForeignKey('creations.id'), nullable=False)
    title = db.Column('title', db.String(255))
    comment = db.Column('comment', db.String(255))
    reference = db.Column('reference', db.Integer, nullable=False)
    posted_at = db.Column(db.DateTime)
    fetched_at = db.Column(db.DateTime)
    
    # Relationships
    contents = db.relationship("PostContent", backref="post", cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
    
    def get_content(self):
        """getter for creation"""
        content = self.contents
        if content is not None and len(content) > 0:
            return content[-1]
        return None
        
    def has_content(self):
        content = self.contents
        if content is not None and len(content) > 0:
            return True
        return False
