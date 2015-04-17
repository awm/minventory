import os
import datetime
from base64 import standard_b64encode

from werkzeug import generate_password_hash
from flask import request, session

from flask.ext.login import UserMixin, login_user, logout_user

from app import app, db, Base

def _get_session_token():
    if 'token' in session:
        return session['token']
    elif 'Authorization' in request.headers:
        auth_parts = request.headers['Authorization'].split(' ')
        if auth_parts[0] == "minventory-token" and len(auth_parts) == 2:
            token_parts = auth_parts[1].split('=', 1)
            if token_parts[0] == "token" and len(token_parts) == 2:
                return token_parts[1]
    return None

# Define a User model
class User(Base, UserMixin):
    __tablename__ = "auth_user"
    id       = db.Column(db.Integer(),    primary_key=True)
    name     = db.Column(db.String(128),  nullable=False)
    username = db.Column(db.String(128),  nullable=False, unique=True)
    email    = db.Column(db.String(128),  nullable=False)
    password = db.Column(db.String(192),  nullable=False)
    active   = db.Column(db.Boolean(),    nullable=False, default=True)

    def __init__(self, name, username, email, password, active=True):
        self.name     = name
        self.username = username
        self.email    = email
        self.password = generate_password_hash(password, method=app.config['PW_HASH_SETTINGS'], salt_length=app.config['PW_SALT_LENGTH'])
        self.active   = active

    def __repr__(self):
        return "User<username={0}>".format(self.username)

    @staticmethod
    def get(user_id):
        return User.query.filter_by(id=user_id).first()

    def is_authenticated(self):
        token = _get_session_token()
        if token is not None:
            sessions = [s for s in self.sessions if s.token == token]
            saved_session = sessions[0] if sessions else None
            return False if saved_session is None else saved_session.validate()
        return False

    def is_active(self):
        return self.active

    def start_session(self):
        saved_session = Session(self)
        session['user_id'] = self.id
        session['token'] = saved_session.token
        login_user(self)
        db.session.add(saved_session)
        db.session.commit()

    def end_session(self):
        token = _get_session_token()
        if token:
            sessions = [s for s in self.sessions if s.token == token]
            saved_session = sessions[0] if sessions else None
            if saved_session is not None:
                saved_session.invalidate()
        logout_user()

class Session(Base):
    __tablename__ = "auth_session"
    id      = db.Column(db.Integer(), primary_key=True)
    token   = db.Column(db.String(192), nullable=False, unique=True)
    expires = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('auth_user.id'))
    user    = db.relationship(User, backref="sessions")

    def __init__(self, user, token=None, expires=(datetime.datetime.utcnow() + datetime.timedelta(minutes=10))):
        if token is None:
            token = Session.generate_token()

        self.user = user
        self.token = token
        self.expires = expires

    @staticmethod
    def generate_token():
        data = os.urandom(32)
        return standard_b64encode(data)

    def __repr__(self):
        return "Session<user={0}, expires={1}>".format(self.user, self.expires)

    def validate(self):
        if datetime.datetime.utcnow() < self.expires:
            return True
        else:
            self.invalidate()

    def invalidate(self):
        db.session.delete(self)
        db.session.commit()
