#!/usr/bin/python3
"""Test script to verify Flask-SQLAlchemy models"""

from flask_app import app
from models import db

with app.app_context():
    print("Database URI:", app.config.get('SQLALCHEMY_DATABASE_URI'))
    print("Models imported successfully")
    
    # Test creating tables
    try:
        db.create_all()
        print("Tables created successfully")
    except Exception as e:
        print("Error creating tables:", e) 