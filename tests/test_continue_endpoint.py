from flask import Flask
from models import db
from models.user import User
from models.creator import Creator
from models.creation import Creation
from models.post import Post
from models.user_creation import UserPostProgress


def test_continue_redirect(app=None):
    # Reuse the app fixture by manually creating a new Flask app similar to other tests
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
        # create user, creator, creation, posts
        user = User(username='tester2', email='t2@test.com')
        user.set_password('pass')
        db.session.add(user)
        creator = Creator(reference=1, name='c2', link='http://example.com')
        db.session.add(creator)
        db.session.commit()
        creation = Creation(creator_id=creator.id, name='C2')
        db.session.add(creation)
        db.session.commit()
        posts = []
        for i in range(1, 5):
            p = Post(creation_id=creation.id, title=f'Post{i}', reference=i)
            db.session.add(p)
            posts.append(p)
        db.session.commit()

        # mark first two posts as read
        for p in posts[:2]:
            upp = UserPostProgress(user_id=user.id, post_id=p.id, is_read=True)
            db.session.add(upp)
        db.session.commit()

        # set per-creation progress to reference 2
        user.set_creation_progress(creation.id, last_post_id=posts[1].id, last_reference=2)

        # Now simulate the continue logic manually: should point to reference 3 (posts[2])
        prog = user.get_creation_progress(creation.id)
        assert prog.last_reference == 2
        # find next
        posts_sorted = sorted(creation.posts, key=lambda p: p.reference)
        next_post = None
        for p in posts_sorted:
            if p.reference > prog.last_reference:
                next_post = p
                break
        assert next_post is not None
        assert next_post.reference == 3
