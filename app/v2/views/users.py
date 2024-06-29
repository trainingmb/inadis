#!/usr/bin/python3
"""
API Base for Users based actions
"""
from app.v2.views import app_views, jsonify, abort, flash, redirect,request, render_template, url_for
from models import storage
from app.v2.views import BaseUserForm
from flask_login import login_required, current_user
from models.user import User


@app_views.route('/user/profile')
@login_required
def userprofile():
    return render_template('user/userprofile.html', user=current_user)


@app_views.route('/user/profile/deleteapikey')
@login_required
def user_deleteapi():
    current_user.delete_apikey()
    current_user.save()
    return redirect(url_for('app_views.userprofile'))

@app_views.route('/user/profile/genapikey')
@login_required
def user_genapi():
    current_user.generate_apikey()
    current_user.save()
    return redirect(url_for('app_views.userprofile'))