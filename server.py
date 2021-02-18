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
                
                session['user'] = user.user_id                
                
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
    del session['user']
    logout_user()
    return redirect(url_for('index'))

#====================== Getting data for testing and vaccine locations =====================#
def format_data(d, key):
    """Formats database data to in dict format
    
    Parameters:
    -----------
    d: crud query results

    key: string
        values: ('test_id', 'vaccine_id')

    Returns:
        dict
        Returns a dict() of the query results from the testing or vaccine data.
    
    """
    # Checks to see if the key passed in matches the primary key from the
    # VaccineLocation or TestingLocation model.
    assert key in ['test_id', 'vaccine_id'], "Please use the correct attribute."

    # This will hold our data from the crud query.
    data = {}

    # row is the query object that is returned from crud.
    # Remeber that d is the query results that come in as a list of query objects.
    for row in d:
        # r is a temporary variable that will hold the attributes for each test_id/vaccine_id
        # For example, r will store the {'address': '1725 S Bascom'} for each key value pair
        # found in the object. This connects back to the repr that is defined in the model.py
        r = {}

        # Here we use dir to return all the attributes associated with the object row (query object).
        for attribute in dir(row):

            # Here is a list of attributes that we would like to ignore.
            if not (
                    attribute.startswith('__') or attribute.startswith('_') or \
                    attribute.startswith('query') or attribute.startswith('metadata') or \
                    attribute.startswith(key)
                    ):

                # For all other attributes we want to add them to our `r` dictionary. 
                # We use the getattr builtin function to return the value for an attribute from a given object.
                # This is similar to using row.attribute dot access. For example, if you wanted to get the address
                # from a query object you would access it with testing_info.address but instead we format like this
                # getattr(testing_info, 'address')

                r[attribute] = getattr(row, attribute)

                # Printing the attributes to make sure we are not bringing in anything we don't want.
                print('***', str(attribute), '***')
        # Lastly, we want to tie each r dict(), that stores our data, to the test_id/vaccine_id found in our `key` parameter.

        data[getattr(row, key)] = r
    # Return the dict data to the app.
    return data 
    

#====================== Testing =====================#
@app.route('/testing', methods=['GET', 'POST'])
def search_testing():
    """Return an address for this zipcode"""

    zip_code = request.args.get('zipcode') 
    testing_info = crud.get_testing_location_by_zipcode(zip_code)
    data = format_data(d=testing_info, key='test_id')
    # if 'user' in session:
    #     print(session['user'])
    if 'user' in session:
        user_id = session['user']
    else:
        user_id = None
    return render_template('testing.html', data=data, user_id=user_id)


#====================== Saved Testing Locations =====================#
@app.route('/add_testing_location')
def add_testing_location(test_id):

    """Add a test location to profile and redirect to profile page.

    When a location is added to the profile, redirect browser to the profile
    page and display a confirmation message: 'Location just added to your profile.'."""



    # Show user success message on next page load
    flash("The vaccine location just added to your profile.")


    return redirect('/profile')    


#====================== Vaccine =====================#
@app.route('/vaccine', methods=['GET', 'POST'])
def search_vaccine():
    """Return an address for this zipcode"""

    zip_code = request.args.get('zipcode') 
    vaccine_info = crud.get_vaccine_location_by_zipcode(zip_code)
    data = format_data(d=vaccine_info, key='test_id')

    # if 'user' in session:
    #     print(session['user'])
    if 'user' in session:
        user_id = session['user']
    else:
        user_id = None

    return render_template('vaccine.html', data=data, user_id=user_id)


#====================== Saved Vaccine Locations =====================#
@app.route('/add_vaccine_location')
def add_saved_location(vaccine_id):

    """Add a vaccine location to profile and redirect to profile page.

    When a location is added to the profile, redirect browser to the profile
    page and display a confirmation message: 'Location just added to your profile.'."""

    # Check if we have a cart in the session and if not, add one
    # Also, bind the cart to the name 'cart' for easy reference below
    if 'cart' in session:
        cart = session['cart']
    else:
        cart = session['cart'] = {}

    # We could also do this with setdefault:
    # cart = session.setdefault("cart", {})

    # Add melon to cart - either increment the count (if melon already in cart)
    # or add to cart with a count of 1
    cart[location_id] = cart.get(vaccine_id, 0) + 1

    # Print cart to the terminal for testing purposes
    # print("cart:")
    # print(cart)

    # Show user success message on next page load
    flash("The vaccine location just added to your profile.")


    return render_template('/profile')


#====================== Symptom's Tracker =====================#
@app.route('/symptom-tracker')
def symptom_tracker():


    return render_template('symptom-tracker.html')

#====================== Profile =====================#
@app.route('/profile')
@login_required
def profile():
    """Display all saved locations and symptom's Tracker"""



    return render_template('profile.html')



if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug=True, port="8080")

