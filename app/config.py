#!/usr/bin/python3
# config.py

"""
Module containing the configurations for different environments
"""

import os

class Config(object):
    """Common configurations"""
    # Put any configurations common across all environments
    SESSION_COOKIE_NAME = "session"
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', 'file.db')


class DevelopmentConfig(Config):
    """Development configurations"""
    DEBUG = True  # activates debug mode on app
    SQLALCHEMY_ECHO = True  # allows SQLAlchemy to log errors
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # allows SQLAlchemy to track changes while running


class ProductionConfig(Config):
    """Production configurations"""
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app_config = {
    'development': 'DevelopmentConfig',
    'production': 'ProductionConfig'
}