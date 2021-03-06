from CovidTracker.app import app 
from CovidTracker.crud.testing import get_testing_location_by_zipcode, get_testing_location_by_test_id, check_testing_saved_location_in_favorites, create_testing_saved_locations

from CovidTracker.helper import format_data 
from flask import (render_template, request, session)


@app.route('/testing')
def search_testing():
    """Get list of testing locations"""

    zip_code = request.args.get('zip_code')
    testing_info = get_testing_location_by_zipcode(zip_code)
    data = format_data(d=testing_info, key='test_id')

    if 'user_id' in session:
        user_id = session['user_id']
    else:
        
        user_id = None
        
    return render_template('testing.html', data=data, user_id=user_id)



@app.route('/add_testing_site', methods=['POST'])
def add_testing_site():
    """Add testing location to the database"""

    test_id = request.form.get('test_id')
    favorite = { 
                    'status': None,
                }
    try:
        if 'user_id' in session:
            user_id = session['user_id']

            already_favorited = check_testing_saved_location_in_favorites(user_id, test_id)

            if already_favorited:
                favorite['status'] = 'already_favorited'
                flash('Already saved to favorites.')
                return favorite

            else:
                favorite['status'] = 'added'
                saved_location = create_testing_saved_locations(user_id, test_id) 
                location = get_testing_location_by_test_id(test_id)
                flash(f'Testing Location {location.alternate_name} saved to profile!')
                return favorite 


        else:
            flash('Please login to save a location!')

        return render_template('testing.html', data=data, user_id=user_id)

    except Exception as e:
        msg = f"Error. Tried adding {test_id} to db failed: \n {e}."
        return msg 

    return msg 