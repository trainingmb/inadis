#!/usr/bin/python3
""" holds class Creator"""

from .base_model import BaseModel
from . import db


class Creator(BaseModel):
    """Representation of a creator """
    __tablename__ = 'creators'
    
    reference = db.Column('reference', db.Integer, nullable=False)
    name = db.Column('name', db.String(128), nullable=False)
    link = db.Column('link', db.String(255), nullable=False)
    creations = db.relationship("Creation", backref="creator", cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)