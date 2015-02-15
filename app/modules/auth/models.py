# Import password / encryption helper tools
from werkzeug import generate_password_hash

from flask.ext.login import UserMixin

from app import app, db, Base

# Define a User model
class User(Base, UserMixin):
    __tablename__ = 'auth_user'

    # Unique ID
    id       = db.Column(db.Integer(),    primary_key=True)

    # User Name
    name     = db.Column(db.String(128),  nullable=False)

    # Identification Data: username, email & password
    username = db.Column(db.String(128),  nullable=False,
                                          unique=True)
    email    = db.Column(db.String(128),  nullable=False)
    password = db.Column(db.String(192),  nullable=False)

    # New instance instantiation procedure
    def __init__(self, name, username, email, password):
        self.name     = name
        self.username = username
        self.email    = email
        self.password = generate_password_hash(password)

    def __repr__(self):
        return '<User %r>' % (self.name)

    @staticmethod
    def get(user_id):
        return User.query.filter_by(id=user_id).first()
