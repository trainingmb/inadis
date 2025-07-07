#!/usr/bin/python3
# config.py

"""
Module containing the configurations for different environments
"""

import os



def read_from_conifg():
    """
    Reads the database URL from a config file if it exists.
    :return: Database URL or None
    """
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', 'db.config')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            for line in f:
                if line.startswith('SQLALCHEMY_DATABASE_URI'):
                    return line.split('=')[1].strip().strip('"').strip("'")
    return None


class Config(object):
    """Common configurations"""
    # Put any configurations common across all environments
    SESSION_COOKIE_NAME = "session"
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              read_from_conifg() or \
                              'sqlite:///' + os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', 'file.db')


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
