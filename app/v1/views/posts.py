#!/usr/bin/python3
"""
API Base for Creations based actions
"""
from app.v1.views import app_views, jsonify, abort, redirect,request, render_template, url_for
from app.v1.views import BasePostForm
from models import storage
from models.creator import Creator
from models.creation import Creation
from models.post import Post


@app_views.route('/posts', methods=['GET'], strict_slashes=False)
def all_posts():
    """
    Returns a list of all posts
    """
    all_posts = storage.all_select(Post, 
                [Post.id, Post.creation_id, Post.title, Post.comment, Post.reference, Post.posted_at, Post.fetched_at]).values()
    posts=[{'id':i.id, 'title':i.title, 'reference': i.reference} for i in sorted(all_posts, key=lambda i:i.reference)]
    return render_template('user/list_posts.html', posts = posts)

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
            newpost_obj = Post(creation_id=creation_id, title=form.post_title.data,
                                   content=form.post_content.data, comment=form.post_comment.data,
                                   reference=form.post_reference.data, posted_at=form.post_posted_at.data,
                                   fetched_at=form.post_fetched_at.data)
            newpost_obj.save()
            return redirect(url_for('app_views.rud_post', creator_id=creator_id, creation_id=creation_obj.id, post_id=newpost_obj.id))
    
    form.post_creations.data = creation_obj.id
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
        return redirect(url_for('app_views.all_posts'))
    if request.method == 'POST':
        if form.validate_on_submit():
            post_obj.title = form.post_title.data
            post_obj.content = form.post_content.data
            post_obj.comment = form.post_comment.data
            post_obj.reference = form.post_reference.data
            post_obj.posted_at = form.post_posted_at.data
            post_obj.fetched_at = form.post_fetched_at.data
            if form.post_creations.data != creation_obj.id and form.post_creations.data in \
                [i[0] for i in choices]:
                    post_obj.creation_id = form.post_creations.data
            post_obj.save()
    form.post_title.data = post_obj.title
    form.post_content.data = post_obj.content
    form.post_comment.data = post_obj.comment
    form.post_reference.data = post_obj.reference
    form.post_posted_at.data = post_obj.posted_at
    form.post_fetched_at.data = post_obj.fetched_at
    form.post_creations.data = post_obj.creation_id
    form.submit.label.text = "Save Changes"
    return render_template('user/post_view.html', creator_obj=creator_obj, creation=creation_obj, post=post_obj, form=form)
