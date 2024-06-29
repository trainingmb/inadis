#!/usr/bin/python3
"""
API Base for Creations based actions
"""
from app.v2.views import app_views, jsonify, abort, redirect,request, render_template, url_for
from app.v2.views import BasePostForm
from models import storage
from models.creator import Creator
from models.creation import Creation
from models.post import Post
from models.post_content import PostContent
from datetime import datetime


@app_views.route('/posts', methods=['GET'], strict_slashes=False)
def all_posts():
    """
    Returns a list of all posts
    """
    all_creations = {}
    for i in storage.all(Creation).values():
        all_creations[i.id] = i
    all_posts = storage.all_select(Post, 
                [Post.id, Post.creation_id, Post.title, Post.comment, Post.reference, Post.posted_at, Post.fetched_at]).values()
    posts=[i for i in sorted(all_posts, key=lambda i:(i.creation_id, i.reference))]
    return render_template('user/list_posts.html', posts=posts, creations=all_creations)

@app_views.route('/creators/<creator_id>/creations/<creation_id>/newpost', methods=['POST', 'GET'], strict_slashes=False)
def create_post(creator_id, creation_id):
    """
    Create a New Post
    """
    creator_obj = storage.get(Creator, creator_id)
    if creator_obj is None:
        abort(404, "Creator not Found")
    creation_obj = storage.get(Creation, creation_id)
    if creation_obj is None or creation_obj.creator_id != creator_obj.id:
        abort(404, "Creation not Found")
    form = BasePostForm()
    form.post_creations.choices = [(creation_obj.id,creation_obj.name)]
    if request.method == 'POST':
        if form.validate_on_submit():
            newpost_obj = Post(creation_id=creation_id, title=form.post_title.data, comment=form.post_comment.data,
                                   reference=form.post_reference.data, posted_at=form.post_posted_at.data,
                                   fetched_at=form.post_fetched_at.data)
            newpost_obj.save()
            newpostcontent_obj = PostContent(post_id=newpost_obj.id, content=form.post_content.data)
            newpostcontent_obj.save()
            return redirect(url_for('app_views.rud_post', creator_id=creator_id, creation_id=creation_obj.id, post_id=newpost_obj.id))
    
    form.post_creations.data = creation_obj.id
    form.post_posted_at.data = datetime.now()
    form.post_fetched_at.data = datetime.now()
    return render_template('user/create_post.html', creator=creator_obj, creation=creation_obj, form=form)

@app_views.route('/creators/<creator_id>/creations/<creation_id>/posts/<post_id>', methods=['POST', 'GET', 'DELETE'])
def rud_post(creator_id, creation_id, post_id):
    """
    Get/Modify/Delete post with id <post_id>
    if present else returns raises error 404
    """
    creator_obj = storage.get(Creator, creator_id)
    if creator_obj is None:
        abort(404, "Creator not Found")
    creation_obj = storage.get(Creation, creation_id)
    if creation_obj is None or creation_obj.creator_id != creator_obj.id:
        abort(404, "Creation not Found")
    post_obj = storage.get(Post, post_id)
    if post_obj is None or creation_obj.id != post_obj.creation_id:
        abort(404, "Post not Found")
    form = BasePostForm()
    choices = [(cr.id, cr.name) for cr in storage.all(Creation).values()]
    form.post_creations.choices = choices
    if '_method' in request.form.keys() and request.form['_method'] == 'DELETE':
        post_obj.delete()
        storage.save()
        return redirect(url_for('app_views.rud_creation', creator_id=creator_obj.id, creation_id=creation_obj.id))
    if request.method == 'POST':
        if form.validate_on_submit():
            post_obj.title = form.post_title.data
            post_obj.comment = form.post_comment.data
            post_obj.reference = form.post_reference.data
            post_obj.posted_at = form.post_posted_at.data
            post_obj.fetched_at = form.post_fetched_at.data
            if form.post_creations.data != creation_obj.id and form.post_creations.data in \
                [i[0] for i in choices]:
                    post_obj.creation_id = form.post_creations.data
            content = post_obj.get_content()
            if content is None:
                newpostcontent_obj = PostContent(post_id=post_obj.id, content = form.post_content.data)
                newpostcontent_obj.save()
            else:
                content.content = form.post_content.data
                content.save()
            post_obj.save()
    form.post_title.data = post_obj.title
    content = post_obj.get_content()
    if content is None:
        form.post_content.data = ""
    else:
        form.post_content.data = content.content
    form.post_comment.data = post_obj.comment
    form.post_reference.data = post_obj.reference
    form.post_posted_at.data = post_obj.posted_at
    form.post_fetched_at.data = post_obj.fetched_at
    form.post_creations.data = post_obj.creation_id
    form.submit.label.text = "Save Changes"
    return render_template('user/post_view.html', creator_obj=creator_obj, creation=creation_obj, post=post_obj, content=post_obj.get_content(), form=form)

@app_views.route('/creators/<creator_id>/creations/<creation_id>/posts/<post_id>/next', methods=['GET'])
def get_next_post(creator_id, creation_id, post_id):
    """
    Get Next Post
    """
    creator_obj = storage.get(Creator, creator_id)
    if creator_obj is None:
        abort(404, "Creator not Found")
    creation_obj = storage.get(Creation, creation_id)
    if creation_obj is None or creation_obj.creator_id != creator_obj.id:
        abort(404, "Creation not Found")
    post_obj = storage.get(Post, post_id)
    if post_obj is None or creation_obj.id != post_obj.creation_id:
        abort(404, "Post not Found")
    next_p = creator_obj.get_next_post(post_id)
    if next_p is None:
        return redirect(url_for('app_views.rud_post', creator_id=creator_id, creation_id=creation_id, post_id=post_id))
    else:
        return redirect(url_for('app_views.rud_post', creator_id=creator_id, creation_id=creation_id, post_id=next_p))