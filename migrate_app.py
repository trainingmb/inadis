#!/usr/bin/python3
"""Standalone Flask app for migrations"""

import os
from flask import Flask
from flask_migrate import Migrate
from models import db

# Import all models
from models.user import User
from models.creator import Creator
from models.creation import Creation
from models.post import Post
from models.post_content import PostContent
from models.user_creation import UserCreation

def create_migrate_app():
    """Create Flask app for migrations"""
    app = Flask(__name__)
    
    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///instance/file.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    
    return app

app = create_migrate_app()

if __name__ == '__main__':
    app.run(debug=True) 