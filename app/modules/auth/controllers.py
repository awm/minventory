# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import Login
from flask.ext.login import LoginManager, login_required

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import application instance
from app import app

# Import module forms
from app.modules.auth.forms import LoginForm

# Import module models (i.e. User)
from app.modules.auth.models import User

# Set up the login manager
login_manager = LoginManager()
login_manager.init_app(app)

# Register the login callback
@login_manager.user_loader
def load_user(userid):
    return User.get(userid)

# Define the blueprint: 'auth'
mod_auth = Blueprint('auth', __name__, template_folder='templates')

# Set the route and accepted methods
@mod_auth.route('/login', methods=['GET', 'POST'])
def signin():
    # If sign in form is submitted
    form = LoginForm(request.form)

    # Verify the sign in form
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            login_user(user)
            flash("Logged in successfully.")
            return redirect(request.args.get("next") or url_for("index"))
        flash('Incorrect user name or password', 'error-message')

    return render_template("auth/login.html", form=form)

@mod_auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.signin'))
