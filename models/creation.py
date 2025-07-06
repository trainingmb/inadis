#!/usr/bin/python3
""" holds class Creation"""

from .base_model import BaseModel
from . import db


class Creation(BaseModel):
    """Representation of a creation """
    __tablename__ = 'creations'
    
    creator_id = db.Column('creatorid', db.String(60), db.ForeignKey('creators.id'), nullable=False)
    regexfilter = db.Column('regexfilter', db.String(255))
    name = db.Column('name', db.String(255), nullable=True)
    
    # Relationships
    posts = db.relationship("Post", backref="creation", cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    @property
    def posts_no_content(self):
        """getter for list of posts related to the Creation"""
        all_posts = self.posts
        if all_posts is not None:
            return sorted(all_posts, key=lambda i:i.reference)
        return None

    @property
    def latest_post(self):
        p = self.posts_no_content
        if p == []:
            return None
        else:
            return p[-1]
            
    def next_post(self, post_id=''):
        p = [i.id for i in self.posts_no_content]
        if p == [] or post_id == '':
            return None
        else:
            try:
                n = p.index(post_id)
                if n > 0:
                    return p[n-1]
            except ValueError:
                return None
        return None
        
    def prev_post(self, post_id=''):
        p = [i.id for i in self.posts_no_content]
        if p == [] or post_id == '':
            return None
        else:
            try:
                n = p.index(post_id)
                if n < (len(p) - 1):
                    return p[n+1]
            except ValueError:
                return None
        return None
