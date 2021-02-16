import crud
import login_form
from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


app = Flask(__name__)
app.secret_key = "dev"
bootstrap = Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return crud.get_user_by_id(user_id)


@app.route('/')
def landingpage():
    """View Landing Page"""

    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = login_form.LoginForm()

    if form.validate_on_submit():
        user = crud.get_user_by_username(username=form.username.data)
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect('profile')

        return '<h1>Invalid username or password</h1>'
        # return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    form = login_form.RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        crud.create_user(username=form.username.data, email=form.email.data, password=hashed_password)

        return '<h1>New user has been created!</h1>'
        # return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)


@app.route('/profile')
@login_required
def profile():

    return render_template('profile.html')


# @app.route('/logout')
# @login_required
# def logout():

#     logout_user()
#     return redirect(url_for('index'))

    


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True, port="8080")

