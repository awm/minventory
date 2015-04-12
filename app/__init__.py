from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Configuration
app.config.from_object('config')
app.config['PW_HASH_SETTINGS'] = "pbkdf2:sha256:10000"
app.config['PW_SALT_LENGTH'] = 32

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Define a base model for other database tables to inherit
class Base(db.Model):
    __abstract__ = True
    id            = db.Column(db.Integer(),     primary_key=True)
    date_created  = db.Column(db.DateTime(),    default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime(),    default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

# Import a module / component using its blueprint handler variable (mod_auth)
from app.modules.auth.controllers import mod_auth, login_required

@app.route("/")
@login_required
def index():
    return "Hello, World!"

# Register blueprint(s)
app.register_blueprint(mod_auth, url_prefix="/auth")
# app.register_blueprint(xyz_module)
# ..
