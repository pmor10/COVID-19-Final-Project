from CovidTracker.app import app 
from CovidTracker.crud.vaccine import get_vaccine_location_by_zipcode, get_vaccine_location_by_vaccine_id, del_vaccine_saved_locations, check_vaccine_saved_location_in_favorites, create_vaccine_saved_locations

from CovidTracker.helper import format_data, vaccine_to_geojson
from flask import (render_template, request, session, flash, jsonify)

@app.route('/vaccine')
def search_vaccine():
    """Get list of vaccine locations"""
    zip_code = request.args.get('zip_code')
    vaccine_info = get_vaccine_location_by_zipcode(zip_code)
    
    data = format_data(d=vaccine_info, key='vaccine_id')
    
    if 'user_id' in session:
        user_id = session['user_id']
    else:
        user_id = None

    return render_template('vaccine.html', data=data, user_id=user_id)

@app.route('/get_geojson_by_zip', methods=['GET'])
def get_geojson():
    
    zip_code = request.args.get('zip_code')
    
    vaccine_info = get_vaccine_location_by_zipcode(zip_code)
    
    data = format_data(d=vaccine_info, key='vaccine_id')
    
    # Geo json data 
    geo_data = vaccine_to_geojson(data)

    return geo_data

@app.route('/get_zipcode_data', methods=['GET'])
def get_zipcode_data():

    zip_code = request.args.get('zip_code')
    vaccine_info = get_vaccine_location_by_zipcode(zip_code)
    
    data = format_data(d=vaccine_info, key='vaccine_id')
    
    if 'user_id' in session:
        user_id = session['user_id']
    else:
        user_id = None
    
    for k,v in data.items():
        data[k]['latitude'] = float(str(data[k]['latitude']))
        data[k]['longitude'] = float(str(data[k]['longitude']))

    return jsonify(data)


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

            already_favorited = check_vaccine_saved_location_in_favorites(user_id, vaccine_id)
            
            if already_favorited:
                
                favorite['status'] = 'already_favorited'
                flash('Already saved to favorites.')
                return jsonify(favorite)
            else:
                favorite['status'] = 'added'
                saved_location = create_vaccine_saved_locations(user_id, vaccine_id) 
                location = get_vaccine_location_by_vaccine_id(vaccine_id)
                
                flash('Vaccine Location saved to profile!')
                return jsonify(favorite) 

        else:     
            flash('Please login to save a location!')

    except Exception as e:
        msg = f'Error. Tried adding {vaccine_id} to db failed: \n {e}.'
        return msg 
        
    return jsonify('Success!')




@app.route('/delete_vaccine', methods=['POST'])
def delete_vaccine_loc():
    """ Delete vaccine location from the database """

    user_id = session.get('user_id', None)
    vaccine_id = request.form.get('vaccine_id')
    del_vaccine_saved_locations(user_id, vaccine_id)

    flash("Location removed!")

    return jsonify("Success!")