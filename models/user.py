#!/usr/bin/python3
""" holds class User"""

from .base_model import BaseModel
from flask_login import UserMixin
from secrets import token_hex
from . import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, BaseModel, db.Model):
    """Representation of a User"""
    __tablename__ = 'users'
    
    id = db.Column(db.String(60), primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(128))
    api_key = db.Column(db.String(16), unique=True, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    
    # Relationships
    user_creations = db.relationship("UserCreation", backref="user", cascade="all, delete-orphan")
    followed_creators = db.relationship(
        'UserFollowsCreator',
        backref='user',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    followed_creations = db.relationship(
        'UserFollowsCreation',
        backref='user',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    post_progress = db.relationship(
        'UserPostProgress',
        backref='user',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

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

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


# Add db.Model inheritance after the class is defined
def add_db_model_inheritance():
    from . import db
    User.__bases__ = (UserMixin, BaseModel, db.Model)