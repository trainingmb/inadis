from flask import render_template, request, redirect, url_for, flash, send_file
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.v1.views import app_views, BasePostForm
from models.user import User
from models.creator import Creator
from models.creation import Creation
from models.post import Post
from models import db
from models.user_creation import UserFollowsCreator, UserFollowsCreation, UserPostProgress
from app.v1.forms.postforms import ExportForm
import io
from ebooklib import epub
import zipfile
import tempfile
from datetime import datetime

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
        user = User.query.filter_by(username=username).first()
        # Verify user exists and password matches
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('app_views.user_dashboard'))
        else:
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

@app_views.route('/creators/<string:creator_id>/follow', methods=['POST'])
@login_required
def follow_creator(creator_id):
    if not UserFollowsCreator.query.filter_by(user_id=current_user.id, creator_id=creator_id).first():
        db.session.add(UserFollowsCreator(user_id=current_user.id, creator_id=creator_id))
        db.session.commit()
    return redirect(request.referrer or url_for('app_views.list_creators'))

@app_views.route('/creators/<string:creator_id>/unfollow', methods=['POST'])
@login_required
def unfollow_creator(creator_id):
    rel = UserFollowsCreator.query.filter_by(user_id=current_user.id, creator_id=creator_id).first()
    if rel:
        db.session.delete(rel)
        db.session.commit()
    return redirect(request.referrer or url_for('app_views.list_creators'))

@app_views.route('/creations')
def list_creations():
    creations = Creation.query.all()
    followed_creations = [fc.creation for fc in current_user.followed_creations] if current_user.is_authenticated else []
    return render_template('list_creations.html', creations=creations, followed_creations=followed_creations)

@app_views.route('/creations/<creation_id>/follow', methods=['POST'])
@login_required
def follow_creation(creation_id):
    if not UserFollowsCreation.query.filter_by(user_id=current_user.id, creation_id=creation_id).first():
        db.session.add(UserFollowsCreation(user_id=current_user.id, creation_id=creation_id))
        db.session.commit()
    return redirect(request.referrer or url_for('app_views.list_creations'))

@app_views.route('/creations/<creation_id>/unfollow', methods=['POST'])
@login_required
def unfollow_creation(creation_id):
    rel = UserFollowsCreation.query.filter_by(user_id=current_user.id, creation_id=creation_id).first()
    if rel:
        db.session.delete(rel)
        db.session.commit()
    return redirect(request.referrer or url_for('app_views.list_creations'))

@app_views.route('/creations/<creation_id>')
def creation_view(creation_id):
    creation = Creation.query.get_or_404(creation_id)
    # Use the Creation property which returns posts sorted by reference
    posts = creation.posts_no_content or []
    read_post_ids = set(
        p.post_id for p in UserPostProgress.query.filter_by(user_id=current_user.id, is_read=True).all()
    ) if current_user.is_authenticated else set()
    unread_posts = []
    if current_user.is_authenticated:
        unread_posts = [p for p in posts if p.id not in read_post_ids]
    template = 'user/creation_view.html' if current_user.is_authenticated else 'creation_view.html'
    followed_creations = [fc.creation for fc in current_user.followed_creations] if current_user.is_authenticated else []
    export_form = ExportForm() if current_user.is_authenticated else None
    return render_template(template, creation=creation, posts=posts, read_post_ids=read_post_ids, unread_posts=unread_posts, followed_creations=followed_creations, export_form=export_form)

@app_views.route('/posts/<string:post_id>', methods=['GET', 'POST'])
def post_view(post_id):
    post = Post.query.get_or_404(post_id)
    creation = Creation.query.get(post.creation_id)
    # Order posts by their reference number for consistent navigation
    posts = Post.query.filter_by(creation_id=creation.id).order_by(Post.reference).all()
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
            # Update per-creation progress: set last_post_id and last_reference for this creation
            try:
                current_user.set_creation_progress(creation.id, last_post_id=post.id, last_reference=post.reference)
            except Exception:
                db.session.rollback()
            
            is_read = True
    # provide an edit form to the template (prefilled) so templates expecting 'form' won't error
    try:
        form = BasePostForm()
        form.post_title.data = post.title
        # note: post content may be in PostContent - setting post_content as a string preview
        form.post_content.data = getattr(post, 'content', '')
        form.post_reference.data = post.reference
        form.post_fetched_at.data = post.fetched_at
    except Exception:
        form = None
    return render_template('post_view.html', post=post, creation=creation, prev_post_id=prev_post_id, next_post_id=next_post_id, is_read=is_read, form=form)

@app_views.route('/posts/<string:post_id>/mark_read', methods=['POST'])
@login_required
def mark_post_read(post_id):
    progress = UserPostProgress.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    if not progress:
        progress = UserPostProgress(user_id=current_user.id, post_id=post_id, is_read=True)
        db.session.add(progress)
    else:
        progress.is_read = True
    db.session.commit()
    # Update per-creation progress
    post = Post.query.get(post_id)
    if post:
        try:
            current_user.set_creation_progress(post.creation_id, last_post_id=post.id, last_reference=post.reference)
        except Exception:
            db.session.rollback()
    return redirect(request.referrer or url_for('app_views.post_view', post_id=post_id))


@app_views.route('/export_unread_followed', methods=['GET'])
@login_required
def export_unread_followed():
    """Export unread posts for all creations the user follows.
    Returns a ZIP file containing one EPUB per creation with unread posts.
    """
    try:
        followed = UserFollowsCreation.query.filter_by(user_id=current_user.id).all()
        if not followed:
            flash('You are not following any creations.')
            return redirect(url_for('app_views.user_dashboard'))

        # Prepare temp ZIP
        tmp_buf = io.BytesIO()
        with zipfile.ZipFile(tmp_buf, 'w', zipfile.ZIP_DEFLATED) as zf:
            for rel in followed:
                creation = Creation.query.get(rel.creation_id)
                if not creation:
                    continue
                # unread posts for this creation
                posts = Post.query.filter_by(creation_id=creation.id).order_by(Post.id).all()
                read_ids = set(p.post_id for p in UserPostProgress.query.filter_by(user_id=current_user.id, is_read=True).all())
                unread = [p for p in posts if p.id not in read_ids]
                if not unread:
                    continue
                # build EPUB in memory
                book = epub.EpubBook()
                book.set_identifier(f"creation-{creation.id}")
                book.set_title(f"{creation.name} - Unread Posts")
                book.set_language('en')
                book.add_author(current_user.username)
                chapters = []
                for idx, post in enumerate(unread, 1):
                    c = epub.EpubHtml(title=post.title, file_name=f'chap_{idx}.xhtml', lang='en')
                    c.content = f'<h2>{post.title}</h2><div>{post.content}</div>'
                    book.add_item(c)
                    chapters.append(c)
                book.toc = chapters
                book.spine = ['nav'] + chapters
                book.add_item(epub.EpubNcx())
                book.add_item(epub.EpubNav())
                # write epub to bytes
                epub_buf = io.BytesIO()
                epub.write_epub(epub_buf, book)
                epub_buf.seek(0)
                filename = f"{creation.name.replace(' ', '_')}_unread.epub"
                zf.writestr(filename, epub_buf.read())
        tmp_buf.seek(0)
        ts = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        zip_name = f'unread_followed_{current_user.username}_{ts}.zip'
        return send_file(tmp_buf, as_attachment=True, download_name=zip_name, mimetype='application/zip')
    except Exception as e:
        flash(f'Error exporting unread followed creations: {e}')
        return redirect(url_for('app_views.user_dashboard'))


@app_views.route('/creations/<creation_id>/export_range', methods=['POST'])
@login_required
def export_creation_range(creation_id):
    """Export a range of posts for a given creation. Expects 'start_ref' and 'end_ref' in form.
    """
    start_ref = request.form.get('start_ref')
    end_ref = request.form.get('end_ref')
    try:
        creation = Creation.query.get_or_404(creation_id)
        # find posts by reference
        posts = sorted(creation.posts, key=lambda p: p.reference)
        selected = []
        if start_ref is None or end_ref is None:
            flash('Start and end reference must be provided.')
            return redirect(request.referrer or url_for('app_views.creation_view', creation_id=creation_id))
        try:
            s = int(start_ref)
            e = int(end_ref)
        except ValueError:
            flash('Start and end must be integers.')
            return redirect(request.referrer or url_for('app_views.creation_view', creation_id=creation_id))
        for post in posts:
            if s <= post.reference <= e:
                selected.append(post)
        if not selected:
            flash('No posts found in that range.')
            return redirect(request.referrer or url_for('app_views.creation_view', creation_id=creation_id))
        # build EPUB
        book = epub.EpubBook()
        book.set_identifier(f"creation-{creation.id}-range-{s}-{e}")
        book.set_title(f"{creation.name} - Posts {s} to {e}")
        book.set_language('en')
        book.add_author(current_user.username)
        chapters = []
        for idx, post in enumerate(selected, 1):
            c = epub.EpubHtml(title=post.title, file_name=f'chap_{idx}.xhtml', lang='en')
            c.content = f'<h2>{post.title}</h2><div>{post.content}</div>'
            book.add_item(c)
            chapters.append(c)
        book.toc = chapters
        book.spine = ['nav'] + chapters
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())
        buf = io.BytesIO()
        epub.write_epub(buf, book)
        buf.seek(0)
        filename = f"{creation.name.replace(' ', '_')}_{s}_{e}.epub"
        return send_file(buf, as_attachment=True, download_name=filename, mimetype='application/epub+zip')
    except Exception as e:
        flash(f'Error exporting creation range: {e}')
        return redirect(request.referrer or url_for('app_views.creation_view', creation_id=creation_id))


@app_views.route('/creations/<creation_id>/continue')
@login_required
def continue_creation(creation_id):
    """Redirect the user to the next unread post in a creation.
    Uses UserCreationProgress if present; otherwise falls back to per-post unread detection.
    """
    creation = Creation.query.get_or_404(creation_id)
    # Try per-creation progress
    prog = current_user.get_creation_progress(creation_id)
    posts = sorted(creation.posts, key=lambda p: p.reference)
    next_post = None
    if prog and prog.last_reference is not None:
        # find the post with reference > last_reference
        for p in posts:
            if p.reference > prog.last_reference:
                next_post = p
                break
    if not next_post:
        # fallback: first unread post (based on UserPostProgress)
        read_ids = set(p.post_id for p in UserPostProgress.query.filter_by(user_id=current_user.id, is_read=True).all())
        for p in posts:
            if p.id not in read_ids:
                next_post = p
                break
    if next_post:
        return redirect(url_for('app_views.post_view', post_id=next_post.id))
    flash('No unread posts found for this creation.')
    return redirect(url_for('app_views.creation_view', creation_id=creation_id))


@app_views.route('/following')
@login_required
def following_creations():
    """Show a table of creations the current user follows with most recent read and posts-since counts."""
    followed_rels = UserFollowsCreation.query.filter_by(user_id=current_user.id).all()
    rows = []
    for rel in followed_rels:
        creation = Creation.query.get(rel.creation_id)
        if not creation:
            continue
        # get per-creation progress
        prog = current_user.get_creation_progress(creation.id)
        last_ref = prog.last_reference if prog and prog.last_reference is not None else None
        last_post = None
        if last_ref is not None:
            # find the post with that reference (or the nearest)
            posts = sorted(creation.posts, key=lambda p: p.reference)
            for p in posts[::-1]:
                if p.reference <= last_ref:
                    last_post = p
                    break
        # count posts since last_ref
        if last_ref is None:
            posts_since = len(creation.posts)
        else:
            posts_since = sum(1 for p in creation.posts if p.reference > last_ref)
        rows.append({'creation': creation, 'last_post': last_post, 'posts_since': posts_since})
    return render_template('user/following_creations.html', rows=rows)

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