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
            return sorted(post_list, key=lambda i:i.posted_at, reverse=True)
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
            all_posts = [{'id':i[0], 'creation_id':i[1], 'title':i[2], 'comment':i[3], 'reference':i[4],
                'posted_at':i[5], 'fetched_at':i[6]} for i in models.storage.all_select(Post, 
                [Post.id, Post.creation_id, Post.title, Post.comment, Post.reference, Post.posted_at, Post.fetched_at]).values()]
            print(f"All posts for {self.name} are {len(all_posts)}")
            for post in all_posts:
                if post['creation_id'] == self.id:
                    post_list.append(post)
            print(f"Filtered posts for {self.name} are {len(posts_list)}")
            return sorted(post_list, key=lambda i:i.posted_at, reverse=True)
    @property
    def latest_post(self):
        p = self.posts_no_content
        if p == []:
            return None
        else:
            return p[0]
