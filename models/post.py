#!/usr/bin/python3
""" holds class Post"""

import models
from datetime import datetime
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from hashlib import md5


class Post(BaseModel, Base):
    """Representation of a post"""
    if models.storage_t == 'db':
        __tablename__ = 'posts'
        creation_id = Column('creationid', String(60), ForeignKey('creations.id'), nullable=False)
        creation = relationship('Creation', back_populates='posts')
        title = Column('title', String(255))
        comment = Column('comment', String(255))
        reference = Column('reference', Integer, nullable=False)
        posted_at = Column(DateTime)
        fetched_at = Column(DateTime)
    else:
        creation_id = ""
        title = ""
        comment = ""
        reference = 0
        posted_at = datetime.utcnow()
        fetched_at = datetime.utcnow()

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
    
    def get_content(self):
        """getter for creation"""
        from models.post_content import PostContent
        crtion = models.storage.filtered_get(PostContent, post_id=self.id)
        if crtion is not None and len(crtion) > 1:
            return crtion[-1]
        return crtion
    def has_content(self):
        from models.post_content import PostContent
        crtion = models.storage.filtered_get(PostContent, post_id=self.id)
        if crtion is not None:
            return true
        return false
