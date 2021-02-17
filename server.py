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


#====================== Login =====================#
@app.route('/login', methods=['GET', 'POST'])
def login():

    form = login_form.LoginForm()
    
    if form.validate_on_submit():
        user = crud.get_user_by_username(username=form.username.data)
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect('profile')
        
        flash('Invalid username or password')
        # return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)


#====================== Register =====================#
@app.route('/signup', methods=['GET', 'POST'])
def signup():

    form = login_form.RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        username = crud.get_user_by_username(form.username.data)
        email = crud.get_user_by_email(form.email.data)
        if not username and not email:
            crud.create_user(username=form.username.data, email=form.email.data, password=hashed_password)
            flash('New user has been created!')
        if username:
            flash(f'Username {form.username.data} already exists!')
        
        if email:
            flash(f'Email {form.email.data} already exists!')
                
    return render_template('signup.html', form=form)


#====================== Logout =====================#
@app.route('/logout')
@login_required
def logout():

    logout_user()
    return redirect(url_for('index'))

#====================== Getting data for testing and vaccine locations =====================#
def format_data(d, key):
    assert key in ['test_id', 'vaccine_id'], "Please use the correct attribute."

    data = {}
    for row in d:
        r = {}
        for attribute in dir(row):
            if not (
                    attribute.startswith('__') or attribute.startswith('_') or \
                    attribute.startswith('query') or attribute.startswith('metadata') or \
                    attribute.startswith(key)
                    ):
                r[attribute] = getattr(row, attribute)
                print('***', str(attribute), '***')
        data[getattr(row, attribute)] = r

    return data 
    

#====================== Testing =====================#
@app.route('/testing', methods=['GET', 'POST'])
def search_testing():
    """Return an address for this zipcode"""

    zip_code = request.args.get('zipcode') 
    testing_info = crud.get_testing_location_by_zipcode(zip_code)
    data = format_data(d=testing_info, key='test_id')

    return render_template('testing.html', data=data)


#====================== Vaccine =====================#
@app.route('/vaccine', methods=['GET', 'POST'])
def search_vaccine():
    """Return an address for this zipcode"""

    zip_code = request.args.get('zipcode') 
    vaccine_info = crud.get_vaccine_location_by_zipcode(zip_code)
    data = format_data(d=vaccine_info, key='test_id')

    return render_template('vaccine.html', data=data)


#====================== Saved Locations =====================#
@app.route('/saved_location', methods=['GET', 'POST'])
def saved_location():


    return render_template('saved-location.html')


#====================== Symptom's Tracker =====================#
@app.route('/symptom-tracker')
def symptom_tracker():


    return render_template('symptom-tracker.html')

#====================== Profile =====================#
@app.route('/profile')
@login_required
def profile():
    """Return all saved locations and symptom's Tracker"""

    return render_template('profile.html')



if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True, port="8080")

