#!/usr/bin/python3
""" holds class UserCreation"""

from .base_model import BaseModel
from . import db


class UserCreation(BaseModel):
    """Representation of a user-creation relationship"""
    __tablename__ = 'user_creations'
    
    user_id = db.Column('user_id', db.String(60), db.ForeignKey('users.id'), nullable=False)
    creation_id = db.Column('creation_id', db.String(60), db.ForeignKey('creations.id'), nullable=False)
    
    # Relationships
    creation = db.relationship("Creation")

    def __init__(self, *args, **kwargs):
        """initializes user-creation relationship"""
        super().__init__(*args, **kwargs) 