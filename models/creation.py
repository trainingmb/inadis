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
            return sorted(post_list, key=lambda i:i.reference, reverse=True)
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
            all_posts = models.storage.all_defer(Post, Post.content).values()
            print(f"All posts for {self.name} are {len(all_posts)}")
            for post in all_posts:
                if post.creation_id == self.id:
                    post_list.append(post)
            print(f"Filtered posts for {self.name} are {len(post_list)}")
            return sorted(post_list, key=lambda i:i.reference, reverse=True)
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