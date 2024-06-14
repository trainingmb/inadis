#!/usr/bin/python3
""" holds class post_content"""

import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from hashlib import md5


class PostContent(BaseModel, Base):
    """Representation of a post"""
    if models.storage_t == 'db':
        __tablename__ = 'post_content'
        post_id = Column('postid', String(60), ForeignKey('posts.id'), nullable=False)
        content = Column('content', String(65535))
    else:
        post_id = ""
        content = ""


    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
