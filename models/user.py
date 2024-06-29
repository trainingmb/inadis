#!/usr/bin/python3
""" holds class User"""

import models
from models.base_model import BaseModel, Base
from flask_login import UserMixin
from secrets import token_hex
import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class User(UserMixin, BaseModel, Base):
    """Representation of a User"""
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(100), unique=True)
        password = Column(String(100))
        name = Column(String(128))
        api_key = Column(String(16), unique=True, nullable=True)
        following = relationship("UserCreation",
                                   back_populates="user",
                                   cascade="all, delete, delete-orphan")
    else:
        email = ""
        password = ""
        name = ""
        api_key = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def generate_apikey(self):
        """
        Generate a new API Key
        Cleares out if one in use
        Does not Save to Storage
        """
        self.api_key = token_hex(16)

    def delete_apikey(self):
        """
        Sets the API Key to None
        Does not Save to Storage
        """
        self.api_key = None

    if models.storage_t != "db":
    @property
    def following(self):
        """getter for list of UserCreation Relationship related to the User"""
        from models.user_creation import UserCreation
        return models.storage.filtered_get(UserCreation, user_id=self.id)