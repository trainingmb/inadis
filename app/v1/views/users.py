from flask import render_template, request, redirect, url_for, flash, send_file
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.v1.views import app_views
from models.user import User
from models.creator import Creator
from models.creation import Creation
from models.post import Post
from models import db
from models.user_creation import UserFollowsCreator, UserFollowsCreation, UserPostProgress
import io
from ebooklib import epub

@app_views.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash('Username or email already exists')
            return redirect(url_for('app_views.register'))
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.')
        return redirect(url_for('app_views.login'))
    return render_template('register.html')

@app_views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"Login attempt for username: {username}")
        user = User.query.filter_by(username=username).first()
        print(f"User found: {user}")
        if user:
            print(f"Password check result: {user.check_password(password)}")
            print(f"User password hash: {user.password}")
            print(f"Input password: {password}")
            # Test the password check manually
            manual_check = check_password_hash(user.password, password)
            print(f"Manual password check: {manual_check}")
        if user and user.check_password(password):
            print(f"Login successful for user: {user.username}")
            login_user(user)
            return redirect(url_for('app_views.user_dashboard'))
        flash('Invalid username or password')
    return render_template('login.html')

@app_views.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out')
    return redirect(url_for('app_views.login'))

@app_views.route('/dashboard')
@login_required
def user_dashboard():
    followed_creators = [fc.creator for fc in current_user.followed_creators]
    followed_creations = [fc.creation for fc in current_user.followed_creations]
    post_progress = UserPostProgress.query.filter_by(user_id=current_user.id).all()
    return render_template('user_dashboard.html',
        followed_creators=followed_creators,
        followed_creations=followed_creations,
        post_progress=post_progress)

@app_views.route('/creators')
def list_creators():
    creators = Creator.query.all()
    followed_creators = [fc.creator for fc in current_user.followed_creators] if current_user.is_authenticated else []
    return render_template('list_creators.html', creators=creators, followed_creators=followed_creators)

@app_views.route('/creators/<int:creator_id>/follow', methods=['POST'])
@login_required
def follow_creator(creator_id):
    if not UserFollowsCreator.query.filter_by(user_id=current_user.id, creator_id=creator_id).first():
        db.session.add(UserFollowsCreator(user_id=current_user.id, creator_id=creator_id))
        db.session.commit()
    return redirect(url_for('app_views.list_creators'))

@app_views.route('/creators/<int:creator_id>/unfollow', methods=['POST'])
@login_required
def unfollow_creator(creator_id):
    rel = UserFollowsCreator.query.filter_by(user_id=current_user.id, creator_id=creator_id).first()
    if rel:
        db.session.delete(rel)
        db.session.commit()
    return redirect(url_for('app_views.list_creators'))

@app_views.route('/creations')
def list_creations():
    creations = Creation.query.all()
    followed_creations = [fc.creation for fc in current_user.followed_creations] if current_user.is_authenticated else []
    return render_template('list_creations.html', creations=creations, followed_creations=followed_creations)

@app_views.route('/creations/<int:creation_id>/follow', methods=['POST'])
@login_required
def follow_creation(creation_id):
    if not UserFollowsCreation.query.filter_by(user_id=current_user.id, creation_id=creation_id).first():
        db.session.add(UserFollowsCreation(user_id=current_user.id, creation_id=creation_id))
        db.session.commit()
    return redirect(url_for('app_views.list_creations'))

@app_views.route('/creations/<int:creation_id>/unfollow', methods=['POST'])
@login_required
def unfollow_creation(creation_id):
    rel = UserFollowsCreation.query.filter_by(user_id=current_user.id, creation_id=creation_id).first()
    if rel:
        db.session.delete(rel)
        db.session.commit()
    return redirect(url_for('app_views.list_creations'))

@app_views.route('/creations/<int:creation_id>')
def creation_view(creation_id):
    creation = Creation.query.get_or_404(creation_id)
    posts = Post.query.filter_by(creation_id=creation_id).all()
    read_post_ids = set(
        p.post_id for p in UserPostProgress.query.filter_by(user_id=current_user.id, is_read=True).all()
    ) if current_user.is_authenticated else set()
    unread_posts = []
    if current_user.is_authenticated:
        unread_posts = [p for p in posts if p.id not in read_post_ids]
    template = 'user/creation_view.html' if current_user.is_authenticated else 'creation_view.html'
    return render_template(template, creation=creation, posts=posts, read_post_ids=read_post_ids, unread_posts=unread_posts)

@app_views.route('/posts/<int:post_id>', methods=['GET', 'POST'])
def post_view(post_id):
    post = Post.query.get_or_404(post_id)
    creation = Creation.query.get(post.creation_id)
    posts = Post.query.filter_by(creation_id=creation.id).order_by(Post.id).all()
    idx = [p.id for p in posts].index(post.id)
    prev_post_id = posts[idx-1].id if idx > 0 else None
    next_post_id = posts[idx+1].id if idx < len(posts)-1 else None
    is_read = False
    if current_user.is_authenticated:
        progress = UserPostProgress.query.filter_by(user_id=current_user.id, post_id=post.id).first()
        is_read = progress.is_read if progress else False
        if request.method == 'POST':
            if not progress:
                progress = UserPostProgress(user_id=current_user.id, post_id=post.id, is_read=True)
                db.session.add(progress)
            else:
                progress.is_read = True
            db.session.commit()
            is_read = True
    return render_template('post_view.html', post=post, creation=creation, prev_post_id=prev_post_id, next_post_id=next_post_id, is_read=is_read)

@app_views.route('/posts/<int:post_id>/mark_read', methods=['POST'])
@login_required
def mark_post_read(post_id):
    progress = UserPostProgress.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    if not progress:
        progress = UserPostProgress(user_id=current_user.id, post_id=post_id, is_read=True)
        db.session.add(progress)
    else:
        progress.is_read = True
    db.session.commit()
    return redirect(request.referrer or url_for('app_views.post_view', post_id=post_id))

@app_views.route('/export_epub', methods=['POST'])
@login_required
def export_epub():
    post_ids = request.form.getlist('post_ids')
    mark_as_read = 'mark_as_read' in request.form
    if not post_ids:
        flash('No posts selected for EPUB export.')
        return redirect(request.referrer or url_for('app_views.user_dashboard'))
    try:
        # Fetch posts in the order provided by the user
        posts = Post.query.filter(Post.id.in_(post_ids)).all()
        post_map = {str(p.id): p for p in posts}
        ordered_posts = [post_map[pid] for pid in post_ids if pid in post_map]
        if not ordered_posts:
            flash('Selected posts could not be found.')
            return redirect(request.referrer or url_for('app_views.user_dashboard'))
        # Create EPUB
        book = epub.EpubBook()
        book.set_identifier(f"creation-{ordered_posts[0].creation_id if ordered_posts else 'unknown'}")
        book.set_title(f"EPUB Export - {ordered_posts[0].creation.title if ordered_posts else 'Selection'}")
        book.set_language('en')
        book.add_author(current_user.username)
        chapters = []
        for idx, post in enumerate(ordered_posts, 1):
            c = epub.EpubHtml(title=post.title, file_name=f'chap_{idx}.xhtml', lang='en')
            c.content = f'<h2>{post.title}</h2><div>{post.content}</div>'
            book.add_item(c)
            chapters.append(c)
        book.toc = chapters
        book.spine = ['nav'] + chapters
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())
        # Write to memory
        buf = io.BytesIO()
        epub.write_epub(buf, book)
        buf.seek(0)
        # Mark as read if requested
        if mark_as_read:
            try:
                for post in ordered_posts:
                    progress = UserPostProgress.query.filter_by(user_id=current_user.id, post_id=post.id).first()
                    if not progress:
                        progress = UserPostProgress(user_id=current_user.id, post_id=post.id, is_read=True)
                        db.session.add(progress)
                    else:
                        progress.is_read = True
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                flash(f'Error marking posts as read: {e}')
        filename = f"creation_{ordered_posts[0].creation_id if ordered_posts else 'export'}.epub"
        return send_file(buf, as_attachment=True, download_name=filename, mimetype='application/epub+zip')
    except Exception as e:
        flash(f'Error generating EPUB: {e}')
        return redirect(request.referrer or url_for('app_views.user_dashboard')) 