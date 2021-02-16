from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=256)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=128)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=120)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=256)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=128)])