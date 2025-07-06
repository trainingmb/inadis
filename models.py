#!/usr/bin/python3
"""
Models for Flask-SQLAlchemy
"""

from datetime import datetime
import uuid
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from secrets import token_hex
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship

# This will be initialized by the app
db = SQLAlchemy()

time = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel(db.Model):
    """Base model with common fields"""
    __abstract__ = True
    
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    if key[-3:] == '_at' and type(value) is str:
                        try:
                            setattr(self, key, datetime.strptime(value, time))
                        except ValueError:
                            setattr(self, key, value)
                    else:
                        setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.utcnow()
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def save(self):
        """updates the attribute 'updated_at' with the current datetime"""
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def to_dict(self, save_fs=None):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        if save_fs is None:
            if "password" in new_dict:
                del new_dict["password"]
        return new_dict

    def delete(self):
        """delete the current instance from the storage"""
        db.session.delete(self)
        db.session.commit()


class User(UserMixin, BaseModel):
    """Representation of a User"""
    __tablename__ = 'users'
    
    email = Column(String(100), unique=True)
    password = Column(String(100))
    name = Column(String(128))
    api_key = Column(String(16), unique=True, nullable=True)
    following = relationship("UserCreation",
                               back_populates="user",
                               cascade="all, delete, delete-orphan")

    def generate_apikey(self):
        """Generate a new API Key"""
        self.api_key = token_hex(16)

    def delete_apikey(self):
        """Sets the API Key to None"""
        self.api_key = None


class Creator(BaseModel):
    """Representation of a creator"""
    __tablename__ = 'creators'
    
    reference = Column('reference', Integer, nullable=False)
    name = Column('name', String(128), nullable=False)
    link = Column('link', String(255), nullable=False)
    creations = relationship("Creation",
                          back_populates="creator",
                          cascade="all, delete, delete-orphan")


class Creation(BaseModel):
    """Representation of a creation"""
    __tablename__ = 'creations'
    
    creator_id = Column('creatorid', String(60), ForeignKey('creators.id'), nullable=False)
    creator = relationship('Creator', back_populates='creations')
    regexfilter = Column('regexfilter', String(255))
    name = Column('name', String(255), nullable=True)
    posts = relationship("Post",
                          back_populates="creation",
                          cascade="all, delete, delete-orphan")


class Post(BaseModel):
    """Representation of a post"""
    __tablename__ = 'posts'
    
    creation_id = Column('creationid', String(60), ForeignKey('creations.id'), nullable=False)
    creation = relationship('Creation', back_populates='posts')
    title = Column('title', String(255))
    comment = Column('comment', String(255))
    reference = Column('reference', Integer, nullable=False)
    posted_at = Column(DateTime)
    fetched_at = Column(DateTime)
    
    def get_content(self):
        """getter for post content"""
        content = PostContent.query.filter_by(post_id=self.id).all()
        if content is not None and len(content) > 0:
            return content[-1]
        return None
        
    def has_content(self):
        """check if post has content"""
        content = PostContent.query.filter_by(post_id=self.id).first()
        return content is not None


class PostContent(BaseModel):
    """Representation of post content"""
    __tablename__ = 'post_content'
    
    post_id = Column('postid', String(60), ForeignKey('posts.id'), nullable=False)
    content = Column('content', String(65535))


class UserCreation(BaseModel):
    """Representation of a user-creation relationship"""
    __tablename__ = 'user_creations'
    
    user_id = Column('user_id', String(60), ForeignKey('users.id'), nullable=False)
    creation_id = Column('creation_id', String(60), ForeignKey('creations.id'), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="following")
    creation = relationship("Creation") 