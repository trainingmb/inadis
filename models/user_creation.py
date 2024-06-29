#!/usr/bin/python3
""" holds class User Creation """

import models
from models.base_model import BaseModel, Base
from flask_login import UserMixin
from secrets import token_hex
import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class UserCreation(BaseModel, Base):
    """Representation of a post"""
    if models.storage_t == 'db':
        __tablename__ = 'user_creation'
        user_id = Column('userid', String(60), ForeignKey('user.id'), nullable=False)
        user = relationship('User', back_populates='favourites')
        creation_id = Column('creationid', String(60), ForeignKey('creation.id'), nullable=False)
        creation = relationship('Creation', back_populates='users_following')
    else:
        user_id = ""
        creation_id = ""


    def __init__(self, *args, **kwargs):
        """initializes user following a creation"""
        super().__init__(*args, **kwargs)

    if models.storage_t != "db":
    @property
    def creation(self):
        from models.creation import Creation
        return models.storage.filtered_get(Creation, id=self.creation_id)
    @property
    def user(self):
        from models.user import User
        return models.storage.filtered_get(User, id=self.user_id)
