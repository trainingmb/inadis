import pytest
from flask import Flask
from models import db
from models.user import User
from models.creator import Creator
from models.creation import Creation
from models.post import Post
from models.post_content import PostContent
from models.user_creation import UserPostProgress, UserCreationProgress


@pytest.fixture()
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
        yield app


def test_progress_creation_and_helpers(app):
    with app.app_context():
        # Create user, creator, creation, posts
        user = User(username='tester', email='t@test.com')
        user.set_password('pass')
        db.session.add(user)
        creator = Creator(reference=1, name='c1', link='http://example.com')
        db.session.add(creator)
        db.session.commit()
        creation = Creation(creator_id=creator.id, name='My Creation')
        db.session.add(creation)
        db.session.commit()
        # Create posts with references 1..3
        posts = []
        for i in range(1, 4):
            p = Post(creation_id=creation.id, title=f'P{i}', reference=i)
            db.session.add(p)
            posts.append(p)
        db.session.commit()

        # Initially no progress
        assert user.get_creation_progress(creation.id) is None

        # Use set_creation_progress
        user.set_creation_progress(creation.id, last_post_id=posts[0].id, last_reference=posts[0].reference)
        prog = user.get_creation_progress(creation.id)
        assert prog is not None
        assert prog.last_post_id == posts[0].id
        assert prog.last_reference == 1

        # Mark another post as read via direct UserPostProgress creation (simulate endpoint)
        upp = UserPostProgress(user_id=user.id, post_id=posts[1].id, is_read=True)
        db.session.add(upp)
        db.session.commit()

        # Now update creation progress using helper
        user.set_creation_progress(creation.id, last_post_id=posts[1].id, last_reference=posts[1].reference)
        prog = user.get_creation_progress(creation.id)
        assert prog.last_reference == 2

        # Ensure model exists in DB
        db_prog = UserCreationProgress.query.filter_by(user_id=user.id, creation_id=creation.id).first()
        assert db_prog is not None
        assert db_prog.last_reference == 2
