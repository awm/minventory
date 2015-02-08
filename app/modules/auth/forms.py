# Import Form and RecaptchaField (optional)
from flask.ext.wtf import Form # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, PasswordField, BooleanField

# Import Form validators
from wtforms.validators import InputRequired

# Define the login form (WTForms)
class LoginForm(Form):
    username = TextField('User Name', [InputRequired(message='You must provide a user name.')])
    password = PasswordField('Password', [InputRequired(message='You must provide a password.')])
    remember = BooleanField('Remember Me')
