import os
import crud
import login_form
import binascii
import hashlib
import datetime

from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
from model import connect_to_db

SALT_SIZE = 16

app = Flask(__name__)
app.secret_key = "dev"


@app.route('/')
def index():
    """Display Landing Page"""

    now = datetime.datetime.now().strftime('%B %d, %Y')
    year = datetime.datetime.now().strftime('%Y')
    month = datetime.datetime.now().strftime('%B, %d')



    covid_cases = crud.get_current_covid_data()
    
    death = "{:,.0f}".format(covid_cases.death)

    positive = "{:,.0f}".format(covid_cases.positive)

    hospitalized = "{:,.0f}".format(covid_cases.hospitalizedCurrently)

    totalTestResults = "{:,.0f}".format(covid_cases.totalTestResults)

    return render_template('index.html', now=now,  month=month, year=year, death=death, positive=positive, hospitalizedCurrently=hospitalized, totalTestResults=totalTestResults)


#======================= Signup =====================#
@app.route('/signup', methods=['GET'])
def display_signup_form():
    """ Display sign Up page. """

    return render_template('signup.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """ Sign up new user and then redirect to homepage. """

 
    email = request.form.get('email')
    username = request.form.get('username')

    if username == crud.get_user_by_username(username):
        error = 'User already exists.'
        return render_template('signup.html', error=error)
    else:
        flash('User is available.')

    password = request.form.get('password1')
    salt = binascii.hexlify(os.urandom(SALT_SIZE))
    password_hash = hashlib.sha256(password.encode('utf-8') + salt).hexdigest()

    crud.create_user(username, email, password_hash, salt=salt.decode('utf-8'))
    db_user = crud.get_user_by_username(username)
    session['user_id'] = db_user.user_id
    flash(f'{username} successfully signed up.')
    return redirect('/')


#====================== Login =====================#
@app.route('/login', methods=['GET'])
def display_login_form():
    """ Display log in page. """

    return render_template('login.html')


@app.route('/login', methods=['POST'])
def validate_login_credentials():
    """ Take username and password and validate them. """

    username = request.form.get('username')
    password_entered_plain = request.form.get('password')

    result = {}
    # Does username exist?
    user = crud.get_user_by_username(username)
    if user is None:
        result['username_found'] = False
        result['valid_login'] = None
        return jsonify(result)

    # If yes, does password match username?
    result['username_found'] = True
    salt = user.salt.encode('utf-8')

    password_entered_hash = hashlib.sha256(password_entered_plain.encode('utf-8') + salt).hexdigest()
    password_db_hash =  crud._get_user_password(user.user_id)

    if password_db_hash == password_entered_hash:
        result['valid_login'] = True
        # log user in by assing their id to the session
        session['user_id'] = user.user_id

        return redirect('/user_profile')

        
    else:
        result['valid_login'] = False

    return jsonify(result)


#====================== Logout =====================#
@app.route('/logout')
def logout():
    """ Logout the current logged in user. """
    if 'user_id' in session:

        flash(f'{session["user_id"]} successfully logged out.')
        del session['user_id']

    return redirect('/')
    # return jsonify('logged out')

#=================== User Profile ====================#
@app.route('/user_profile')
def display_user_profile():
    """Display user profile page"""

    if 'user_id' in session:

        user_id = session.get('user_id', None)
        user = crud.get_user_by_id(user_id)
        

        def show_favorites(func1, func2, **kwargs):
            
            favorites = func1(kwargs['user_id'])
            dataset = [] 

            for fav in favorites: 
                row = func2(getattr(fav, kwargs.get('table_id')))

                dataset.append(row)

            return format_data(d=dataset, key=kwargs.get('table_id'))


        vac_data = show_favorites( crud.get_vaccine_saved_locations, 
                            crud.get_vaccine_location_by_vaccine_id,
                            user_id=user_id, 
                            table_id='vaccine_id'
                            )
        
        test_data = show_favorites(crud.get_testing_saved_locations, 
                                   crud.get_testing_location_by_test_id,
                                   user_id=user_id, 
                                   table_id='test_id'
                                    )


        symptom_data = show_favorites(crud.get_symptom_tracker_user_id_symptoms,
                                      crud.get_symptom_by_id,
                                      user_id=user_id, 
                                      table_id='symptom_id'
                                      ) 

        data = {
                'vac_data': vac_data, 
                'test_data': test_data, 
                'symptom_data': symptom_data
                }

        return render_template('user_profile.html', user=user, data=data)

    flash('Sign Up or Log In in order to see your user profile.')
    return redirect('/')


@app.route('/user_profile', methods=['POST'])
def edit_user_profile():
    """Save any changes the user made to their profile"""

    if 'user_id' in session:
        user_id = session.get('user_id')
        email = request.form.get('email')


        flash('User profile saved.')
        return redirect('/')

    flash('Sign Up or Log In in order to see your user profile.')
    return redirect('/')

@app.route('/change_password', methods=['POST'])
def change_password():
    """ Changes user password and redirects to home. """


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
    # assert key in ['test_id', 'vaccine_id', 'symptom_id'], "Please use the correct attribute."

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
                
        # Lastly, we want to tie each r dict(), that stores our data, to the test_id/vaccine_id found in our `key` parameter.

        data[getattr(row, key)] = r
    # Return the dict data to the app.
    return data 
    

#====================== Testing =====================#

@app.route('/testing')
def search_testing():
    """Get list of testing locations"""

    zip_code = request.args.get('zip_code')
    testing_info = crud.get_testing_location_by_zipcode(zip_code)
    data = format_data(d=testing_info, key='test_id')

    if 'user_id' in session:
        user_id = session['user_id']
    else:
        
        user_id = None
        
    return render_template('testing.html', data=data, user_id=user_id)



@app.route('/add_testing_site', methods=['POST'])
def add_testing_site():
    """Add testing location to the database"""
    test_id = request.form.get("test_id")
    favorite = { 
                    'status': None,

                }
    try:
        if 'user_id' in session:
            user_id = session['user_id']

            already_favorited = crud.check_testing_saved_location_in_favorites(user_id, test_id)

            if already_favorited:

                favorite['status'] = 'already_favorited'
                flash('Already saved to favorites.')
                return favorite
            else:
                favorite['status'] = 'added'
                saved_location = crud.create_testing_saved_locations(user_id, test_id) 
                location = crud.get_testing_location_by_test_id(test_id)
                msg = f"Testing Location {location.alternate_name} saved to profile!"
                flash(msg)
                return favorite 


        else:
            msg = "Please login to save a location!"
            flash(msg)
        return render_template('testing.html', data=data, user_id=user_id)


    except Exception as e:
        msg = f"Error. Tried adding {test_id} to db failed: \n {e}."
        return msg 

        
    return msg 
    
#====================== Vaccine =====================#
@app.route('/vaccine')
def search_vaccine():
    """Get list of vaccine locations"""   

    zip_code = request.args.get('zip_code')
    vaccine_info = crud.get_vaccine_location_by_zipcode(zip_code)
    data = format_data(d=vaccine_info, key='vaccine_id')


    if 'user_id' in session:
        user_id = session['user_id']
    else:
        user_id = None
        
    return render_template('vaccine.html', data=data, user_id=user_id)



@app.route('/add_vaccine_site', methods=['POST'])
def add_vaccine_site():
    """Add vaccine location to the database"""

    vaccine_id = request.form.get("vaccine_id")
    favorite = { 
                    'status': None,

                }
    try:
        if 'user_id' in session:
            user_id = session['user_id']

            already_favorited = crud.check_testing_saved_location_in_favorites(user_id, vaccine_id)

            if already_favorited:

                favorite['status'] = 'already_favorited'
                flash('Already saved to favorites.')
                return favorite
            else:
                favorite['status'] = 'added'
                saved_location = crud.create_vaccine_saved_locations(user_id, vaccine_id) 
                location = crud.get_vaccine_location_by_vaccine_id(vaccine_id)
                msg = f"Vaccine Location {location.name} saved to profile!"
                flash(msg)
                return favorite 


        else:
            
            msg = "Please login to save a location!"
            flash(msg)
            # return redirect('/login')
    except Exception as e:
        msg = f"Error. Tried adding {vaccine_id} to db failed: \n {e}."
        return msg 

        
    return msg 


#====================== Symptom's =====================#
@app.route('/symptoms')
def symptom_tracker():
    symptoms = crud.get_symptoms()

    

    return render_template('symptoms.html', symptoms=symptoms)

@app.route('/add_symptoms', methods=['GET', 'POST'])
def add_symptoms():


    if 'user_id' in session:
        user_id = session['user_id']
        msg = "User logged in"
        today = datetime.datetime.now()
        user_symptoms = crud.get_symptom_tracker_user_id_symptoms(user_id)
        
        symptom_count = 0
        for symptom in user_symptoms:
            if datetime.datetime.date(today) == datetime.datetime.date(symptom.symptom_date):
                symptom_count += 1
        
        if symptom_count > 3:
            flash("Please visit your local doctor for a checkup.")

        symptoms = request.form.items()
        
        added_symptoms=[]

        if symptoms:
            for k,v in symptoms:
                try:
                    tracker = crud.create_symptom_tracker(user_id, k)
                    added_symptoms.append(v)
                except:
                    pass 
            
            msg = f"The following symptoms were added to profile: {added_symptoms}"
            return msg

    else:
        
        flash('Please login!')
        msg = "Please login"
        flash(msg) 

    return msg


if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug=True, port="5000")

