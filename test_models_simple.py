#!/usr/bin/python3
"""Simple test script to verify Flask-SQLAlchemy models"""

from flask import Flask
from models import db
from models.user import User
from models.creator import Creator
from models.creation import Creation
from models.post import Post
from models.post_content import PostContent
from models.user_creation import UserCreation

# Create a minimal Flask app for testing
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Flask-SQLAlchemy
db.init_app(app)

with app.app_context():
    print("Database URI:", app.config.get('SQLALCHEMY_DATABASE_URI'))
    print("Models imported successfully")
    
    # Test creating tables
    try:
        db.create_all()
        print("Tables created successfully")
        
        # Test creating a simple object
        creator = Creator(name="Test Creator", reference=123, link="http://test.com")
        db.session.add(creator)
        db.session.commit()
        print("Test creator created successfully")
        
        # Test querying
        creators = Creator.query.all()
        print(f"Found {len(creators)} creators")
        
    except Exception as e:
        print("Error:", e)
        import traceback
        traceback.print_exc() 