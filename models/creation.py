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
            post_list = []
            all_posts = models.storage.all(Post)
            for post in all_posts.values():
                if post.creation_id == self.id:
                    post_list.append(post)
            return post_list
        @property
        def posts_no_content(self):
            """getter for list of posts related to the Creation"""
            post_list = []
            all_posts = models.storage.all(Post)
            for post in all_posts.values():
                if post.creation_id == self.id:
                    post_list.append(post)
            return post_list
        @property
        def creator(self):
            """getter for creator"""
            from models.creator import Creator
            crtor = models.storage.get(Creator, creator_id)
            return crtor
    else:
        @property
        def posts_no_content(self):
            """getter for list of posts related to the Creation"""
            post_list = []
            all_posts = models.storage.all_select(Post, 
                [Post.id, Post.creation_id, Post.title, Post.comment, Post.reference, Post.posted_at, Post.fetched_at])
            for post in all_posts.values():
                if post.creation_id == self.id:
                    post_list.append(post)
            return post_list
