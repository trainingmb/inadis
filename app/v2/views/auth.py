#!/usr/bin/python3
"""
API Base for Users Authentication based actions
"""
from app.v2.views import app_views, jsonify, abort, flash, redirect,request, render_template, url_for
from models import storage
from app.v2.views import BaseUserForm
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User

@app_views.route("/auth/signup", methods=['POST', 'GET'])
def signupUser():
    """
    SignUp a new User
    """
    form  = BaseUserForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            name = form.user_name.data
            email = form.user_email.data
            password = form.user_password.data
            password2 = form.user_password2.data

            if storage.filtered_get(User, **{'email': email}) is not None:
                flash("Email already Exists", "error")
                return redirect(url_for('app_views.signupUser'))
            if password != password2:
                flash("Passwords do not Match", "error")
                return redirect(url_for('app_views.signupUser'))
            newuser_obj = User(name=name, email=email, password=generate_password_hash(password, method='pbkdf2:sha256'))
            newuser_obj.save()
            return redirect(url_for('app_views.loginUser'))
    return render_template('auth/signupUser.html', form=form)

@app_views.route("/auth/login", methods=['POST', 'GET'])
def loginUser():
    """
    Login a new User
    """
    form  = BaseUserForm()
    form.user_name.data = "PLACEHOLDERNAME"
    form.user_password2.data = "PLACEHOLDERPASSWORD"
    form.submit.label.text = "Login User"

    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.user_email.data
            password = form.user_password.data
            remember = True if form.user_remember.data else False
            userSearch = storage.filtered_get(User, **{'email': email})

            if userSearch is None:
                flash("Email Does Not Exist", "error")
                return redirect(url_for('app_views.loginUser'))
            user = userSearch[0]
            if not user or not check_password_hash(user.password, password):
                flash('Please check your login details and try again.')
                return redirect(url_for('auth.login'))
            login_user(user, remember=remember)
            return redirect(url_for('app_views.userprofile'))
    return render_template('auth/loginUser.html', form=form)

@app_views.route("/auth/logout", methods=['GET'])
@login_required
def logoutUser():
    """
    Log Out User
    """
    logout_user()
    return redirect(url_for('app_views.home'))
