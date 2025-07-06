#!/usr/bin/python3
""" holds class User"""

from .base_model import BaseModel
from flask_login import UserMixin
from secrets import token_hex
from . import db


class User(UserMixin, BaseModel):
    """Representation of a User"""
    __tablename__ = 'users'
    
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(128))
    api_key = db.Column(db.String(16), unique=True, nullable=True)
    
    # Relationships
    user_creations = db.relationship("UserCreation", backref="user", cascade="all, delete-orphan")

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

    @property
    def following(self):
        """getter for list of UserCreation Relationship related to the User"""
        return self.user_creations


# Add db.Model inheritance after the class is defined
def add_db_model_inheritance():
    from . import db
    User.__bases__ = (UserMixin, BaseModel, db.Model)