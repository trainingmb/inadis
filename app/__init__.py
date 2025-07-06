#!/usr/bin/python3
# app/__init__.py

import os
from flask import Flask, render_template
from .config import app_config
import importlib

#app = Flask(__name__, template_folder='templates', instance_relative_config=True)

print(u"Current path is", os.path.abspath(os.curdir), sep=' ')


def create_app(config_name = 'development', version = "v1"):
    """
    This is the method that initializes modules used in the app
    :param config_name: The key for the configuration to use
    :return: Flask app
    """
    if config_name not in app_config.keys():
        config_name = 'development'

    app_module = importlib.import_module('app.' + version)
    app = app_module.app
    
    # Load configuration
    config_class = getattr(importlib.import_module('app.config'), app_config[config_name])
    app = app_module.init_app_with_config(config_class)
    
    # use if you have instance/config.py with your SECRET_KEY and SQLALCHEMY_DATABASE_URI
    try:
        app.config.from_pyfile('instance/config.py')
    except FileNotFoundError:
        pass

    return app