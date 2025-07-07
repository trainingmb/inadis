from flask import render_template, request, redirect, url_for, flash
from app.utils.decorators import admin_required
from flask_login import login_required
from app.v1.views import app_views
from models.user import User
from models.creator import Creator
from models.creation import Creation
from models.post import Post
from models import db

@app_views.route('/admin', methods=['GET'])
@admin_required
def admin_dashboard():
    users = User.query.all()
    creators = Creator.query.all()
    creations = Creation.query.all()
    posts = Post.query.all()
    user_count = User.query.count()
    creator_count = Creator.query.count()
    creation_count = Creation.query.count()
    post_count = Post.query.count()
    return render_template('admin/dashboard.html',
                           users=users,
                           creators=creators,
                           creations=creations,
                           posts=posts,
                           user_count=user_count,
                           creator_count=creator_count,
                           creation_count=creation_count,
                           post_count=post_count)

# USERS CRUD
@app_views.route('/admin/users')
@admin_required
def admin_users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@app_views.route('/admin/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.is_admin = 'is_admin' in request.form
        db.session.commit()
        flash('User updated')
        return redirect(url_for('app_views.admin_users'))
    return render_template('admin/edit_user.html', user=user)

@app_views.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def admin_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted')
    return redirect(url_for('app_views.admin_users'))

# CREATORS CRUD
@app_views.route('/admin/creators')
@admin_required
def admin_creators():
    creators = Creator.query.all()
    return render_template('admin/creators.html', creators=creators)

@app_views.route('/admin/creators/<int:creator_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_edit_creator(creator_id):
    creator = Creator.query.get_or_404(creator_id)
    if request.method == 'POST':
        creator.name = request.form['name']
        creator.link = request.form['link']
        db.session.commit()
        flash('Creator updated')
        return redirect(url_for('app_views.admin_creators'))
    return render_template('admin/edit_creator.html', creator=creator)

@app_views.route('/admin/creators/<int:creator_id>/delete', methods=['POST'])
@admin_required
def admin_delete_creator(creator_id):
    creator = Creator.query.get_or_404(creator_id)
    db.session.delete(creator)
    db.session.commit()
    flash('Creator deleted')
    return redirect(url_for('app_views.admin_creators'))

# CREATIONS CRUD
@app_views.route('/admin/creations')
@admin_required
def admin_creations():
    creations = Creation.query.all()
    return render_template('admin/creations.html', creations=creations)

@app_views.route('/admin/creations/<int:creation_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_edit_creation(creation_id):
    creation = Creation.query.get_or_404(creation_id)
    if request.method == 'POST':
        creation.title = request.form['title']
        creation.description = request.form['description']
        db.session.commit()
        flash('Creation updated')
        return redirect(url_for('app_views.admin_creations'))
    return render_template('admin/edit_creation.html', creation=creation)

@app_views.route('/admin/creations/<int:creation_id>/delete', methods=['POST'])
@admin_required
def admin_delete_creation(creation_id):
    creation = Creation.query.get_or_404(creation_id)
    db.session.delete(creation)
    db.session.commit()
    flash('Creation deleted')
    return redirect(url_for('app_views.admin_creations'))

# POSTS CRUD
@app_views.route('/admin/posts')
@admin_required
def admin_posts():
    posts = Post.query.all()
    return render_template('admin/posts.html', posts=posts)

@app_views.route('/admin/posts/<int:post_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        flash('Post updated')
        return redirect(url_for('app_views.admin_posts'))
    return render_template('admin/edit_post.html', post=post)

@app_views.route('/admin/posts/<int:post_id>/delete', methods=['POST'])
@admin_required
def admin_delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted')
    return redirect(url_for('app_views.admin_posts')) 