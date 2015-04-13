import pkgutil

from flask import Blueprint, request, abort, jsonify
from flask.ext.login import LoginManager, login_required

from app import app
from app.modules.auth.models import User

# Read the authorization module configuration
def _get_provider(name):
    fullname = "app.plugins.auth.{}".format(name)
    loader = pkgutil.get_loader(fullname)
    module = loader.load_module(fullname)
    return module

def _configure():
    config = []
    if 'AUTH_PROVIDERS' in app.config:
        for provider in app.config['AUTH_PROVIDERS']:
            if isinstance(provider, list) or isinstance(provider, tuple):
                group = []
                for p in provider:
                    group.append(_get_provider(p))
                config.append(group)
            else:
                config.append([_get_provider(provider)])
    return config
_auth_config = _configure()

# Set up the login manager
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

# Register the login callback
@login_manager.user_loader
def load_user(userid):
    return User.get(int(userid))

# Define the blueprint: 'auth'
mod_auth = Blueprint('auth', __name__)

# Set the route and accepted methods
@mod_auth.route('/login', methods=['POST'])
def login():
    credentials = request.get_json()
    if not credentials or 'username' not in credentials or 'password' not in credentials:
        abort(400)

    authenticated = False
    for providers in _auth_config:
        chain_passed = True
        for provider in providers:
            chain_passed = provider.check(credentials) and chain_passed
        authenticated = chain_passed or authenticated
    if authenticated:
        user = User.query.filter_by(username=credentials['username']).first()
        if user:
            token = user.start_session()
            return jsonify(token=token)
    err = jsonify(error="Authentication failed")
    err.status_code = 401
    return err

@mod_auth.route("/logout")
@login_required
def logout():
    current_user.end_session()
    return ("", 204)
