#!/usr/bin/python3
"""
Simple Flask app for migrations
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Create Flask app
app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/file.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import models after db is initialized
from .models import User, Creator, Creation, Post, PostContent, UserCreation

if __name__ == '__main__':
    app.run(debug=True) 