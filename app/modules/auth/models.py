from app import app, db, Base

# Define a User model
class User(Base):
    __tablename__ = 'auth_user'

    # User Name
    name    = db.Column(db.String(128),   nullable=False)

    # Identification Data: username, email & password
    username = db.Column(db.String(128),  nullable=False,
                                          unique=True)
    email    = db.Column(db.String(128),  nullable=False)
    password = db.Column(db.String(192),  nullable=False)

    # Authorisation Data: role & status
    role     = db.Column(db.SmallInteger, nullable=False)
    status   = db.Column(db.SmallInteger, nullable=False)

    # New instance instantiation procedure
    def __init__(self, name, username, email, password):
        self.name     = name
        self.username = username
        self.email    = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.name)