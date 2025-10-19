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

class UserFollowsCreator(db.Model):
    __tablename__ = 'user_follows_creator'
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), primary_key=True)
    creator_id = db.Column(db.String(60), db.ForeignKey('creators.id'), primary_key=True)
    followed_at = db.Column(db.DateTime, default=db.func.now())

class UserFollowsCreation(db.Model):
    __tablename__ = 'user_follows_creation'
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), primary_key=True)
    creation_id = db.Column(db.String(60), db.ForeignKey('creations.id'), primary_key=True)
    followed_at = db.Column(db.DateTime, default=db.func.now())

class UserPostProgress(db.Model):
    __tablename__ = 'user_post_progress'
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), primary_key=True)
    post_id = db.Column(db.String(60), db.ForeignKey('posts.id'), primary_key=True)
    is_read = db.Column(db.Boolean, default=False)
    read_at = db.Column(db.DateTime) 