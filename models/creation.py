#!/usr/bin/python3
""" holds class Creation"""

import models
from models.base_model import BaseModel, Base
from models.post import Post
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from hashlib import md5


class Creation(BaseModel, Base):
    """Representation of a creation """
    if models.storage_t == 'db':
        __tablename__ = 'creations'
        creator_id = Column('creatorid', String(60), ForeignKey('creators.id'), nullable=False)
        creator = relationship('Creator', back_populates='creations')
        regexfilter = Column('regexfilter', String(255))
        name = Column('name', String(255), nullable=True)
        posts = relationship("Post",
                              back_populates="creation",
                              cascade="all, delete, delete-orphan")
        users_following = relationship('UserCreation', back_populates='creation')
    else:
        creator_id = ""
        regexfilter = ""
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    if models.storage_t != "db":
        @property
        def posts(self):
            """getter for list of posts related to the Creation"""
            return models.storage.filtered_get(Post, creation_id = self.id)
        @property
        def creator(self):
            """getter for creator"""
            from models.creator import Creator
            crtor = models.storage.get(Creator, creator_id)
            return crtor
        @property
        def users_following(self):
            """getter for list of UserCreation Relationship related to the Creation"""
            from models.user_creation import UserCreation
            return models.storage.filtered_get(UserCreation, creation_id = self.id)
        

    @property
    def posts_no_content(self):
        """getter for list of posts related to the Creation"""
        all_posts = models.storage.filtered_get(Post, creation_id = self.id)
        if all_posts is not None:
            return sorted(all_posts, key=lambda i:i.reference, reverse=True)
        return None

    @property
    def latest_post(self):
        p = self.posts_no_content
        if p == []:
            return None
        else:
            return p[0]
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