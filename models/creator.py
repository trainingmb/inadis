#!/usr/bin/python3
""" holds class Creator"""

import models
from models.base_model import BaseModel, Base
from models.creation import Creation
from os import getenv
import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from hashlib import md5


class Creator(BaseModel, Base):
    """Representation of a creator """
    if models.storage_t == 'db':
        __tablename__ = 'creators'
        reference = Column('reference', Integer, nullable=False)
        name = Column('name', String(128), nullable=False)
        link = Column('link', String(255), nullable=False)
        creations = relationship("Creation",
                              back_populates="creator",
                              cascade="all, delete, delete-orphan")
    else:
        reference = 0
        name = ""
        link = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    if models.storage_t != "db":
        @property
        def creations(self):
            """getter for list of creations related to the creator"""
            creation_list = []
            all_creations = models.storage.all(Creation)
            for creation in all_creations.values():
                if creation.creator_id == self.id:
                    creation_list.append(creation)
            return creation_list