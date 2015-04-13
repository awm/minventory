from werkzeug import check_password_hash, generate_password_hash

from app import app
from app.modules.auth.models import User

_default_comparison = generate_password_hash("", method=app.config['PW_HASH_SETTINGS'], salt_length=app.config['PW_SALT_LENGTH'])

def check(credentials):
    user = User.query.filter_by(username=credentials['username']).first()
    pwhash = _default_comparison if user is None else user.password
    result = check_password_hash(pwhash, credentials['password'])
    return result
