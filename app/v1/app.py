#!/usr/bin/python3
"""Version 1 Flask App"""
from flask import Flask, jsonify, render_template
from flask_migrate import Migrate
from models import db
from app.v1.views import app_views
from api.v1.views import api_views
from flask_cors import CORS
from os import  path, curdir, environ
from flask_login import LoginManager

print(u"Current path is", path.abspath(curdir), sep=' ')

app = Flask(__name__, template_folder='templates')

def init_app_with_config(config_object):
    """Initialize the app with configuration"""
    app.config.from_object(config_object)
    # Initialize Flask-SQLAlchemy and Flask-Migrate
    db.init_app(app)
    migrate = Migrate(app, db)
    return app

app.register_blueprint(app_views)
app.register_blueprint(api_views)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(user_id)

# noinspection PyUnresolvedReferences
@app.errorhandler(403)
def forbidden(error):
    return render_template('errors/403.html', title='Forbidden', wrapper='Forbidden', err=error, error=True), 403

# noinspection PyUnresolvedReferences
@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html', title='Page Not Found', wrapper='Page Not Found', err= error, error=True), 404

# noinspection PyUnresolvedReferences
@app.errorhandler(405)
def method_not_allowed(error):
    return render_template('errors/405.html', title='Method Not Allowed', wrapper='Method Not Allowed', err=error, error=True), 404

# noinspection PyUnresolvedReferences
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html', title='Internal Server Error', wrapper='Server Error',
                           error=True), 500

# noinspection PyUnresolvedReferences
@app.errorhandler(401)
def bad_or_missing_authentication(error):
    return render_template('errors/401.html', title='Unauthorized', wrapper="Unauthorized", err=error, error=True), 401

# noinspection PyUnresolvedReferences
@app.errorhandler(503)
def temporarily_unavailable(error):
    return render_template('errors/503.html', title="Temporarily Unavailable", wrapper="Temporarily Unavailable", err=error, error=True), 503

@app.teardown_appcontext
def teardown_db(exception):
    """
    Closes the database session on teardown
    """
    db.session.remove()
