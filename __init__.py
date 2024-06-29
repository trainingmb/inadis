#!/usr/bin/python3
# inadis/__init__.py

import os

from flask import g, Flask, render_template
from flask_login import user_loaded_from_request, LoginManager
from flask.sessions import SecureCookieSessionInterface

# from flask_sqlalchemy import SQLAlchemy
# from flask_bootstrap import Bootstrap

from app.config import app_config
import importlib

def create_login_manager():
    """
    This method generates the login manager its load user method 
    and the unathorised access handler functions. Does not bind
    the manager to an app instance
    :return Login Manager Instance, CustomSessionInterface Class
    """
    login_manager = LoginManager()
    
    @user_loaded_from_request.connect
    def user_loaded_from_request_method(app, user=None):
            g.login_via_request = True


    class CustomSessionInterface(SecureCookieSessionInterface):
        """Prevent creating session from API requests."""
        def save_session(self, *args, **kwargs):
            if g.get('login_via_request'):
                return
            return super(CustomSessionInterface, self).save_session(*args,
                                                                **kwargs)

    return login_manager, CustomSessionInterface


def create_app(config_name, version):
    """
    This is the method that initializes modules used in the app
    :param config_name: The key for the configuration to use
    :return: Flask app
    """
    if config_name not in app_config.keys():
        config_name = 'development'
    api_views = importlib.import_module(f'api.{version}.views').api_views
    app_views = importlib.import_module(f'app.{version}.views').app_views
    app = Flask(__name__, template_folder=f'app/{version}/templates', static_folder=f'app/{version}/static')
    app.config.from_object(".".join(["app", "config", app_config[config_name]]))
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.register_blueprint(api_views)
    app.register_blueprint(app_views)
    app.config['CORS_HEADERS'] = 'Content-Type'
    # use if you have instance/config.py with your SECRET_KEY and SQLALCHEMY_DATABASE_URI
    app.config.from_pyfile(f'app/{version}/instance/config.py')    

    return app