from flask import Blueprint, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from flask_login import LoginManager, login_user, logout_user
from user import User
import requests

import os
from dotenv import load_dotenv

auth_blueprint = Blueprint('auth', __name__)
oauth = OAuth()

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')


def init_oauth(app):
    oauth.init_app(app)

    # Fetch the OpenID Connect discovery document
    discovery_doc = requests.get('https://accounts.google.com/.well-known/openid-configuration').json()

    oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        authorize_params=None,
        access_token_url='https://accounts.google.com/o/oauth2/token',
        access_token_params=None,
        refresh_token_url=None,
        client_kwargs={'scope': 'openid profile email'},
        jwks_uri=discovery_doc['jwks_uri'],  # Manually set the jwks_uri
    )

@auth_blueprint.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('auth.authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@auth_blueprint.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    user_info = google.parse_id_token(token)
    
    # Debugging: print user_info to see what data is returned
    print(user_info)
    
    user = User.get_or_create(user_info)
    login_user(user)
    return redirect(url_for('editor.editor'))

@auth_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
