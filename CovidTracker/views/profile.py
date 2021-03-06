from CovidTracker.app import app 
from CovidTracker.crud.user import get_user_by_id
from CovidTracker.crud.testing import get_testing_saved_locations, get_testing_location_by_test_id
from CovidTracker.crud.vaccine import get_vaccine_saved_locations, get_vaccine_location_by_vaccine_id
from CovidTracker.crud.tracker import get_symptom_tracker_user_id_symptoms
from CovidTracker.crud.symptom import get_symptom_by_id

from CovidTracker.helper import format_data 

from flask import (render_template, session, redirect, flash)


@app.route('/user_profile')
def display_user_profile():
    """Display user profile page"""

    if 'user_id' in session:
        user_id = session.get('user_id', None)
        user = get_user_by_id(user_id)

        def show_favorites(func1, func2, **kwargs):
            
            favorites = func1(kwargs['user_id'])
            dataset = [] 

            for fav in favorites: 
                row = func2(getattr(fav, kwargs.get('table_id')))
                dataset.append(row)

            return format_data(d=dataset, key=kwargs.get('table_id'))

        vac_data = show_favorites(get_vaccine_saved_locations,
                                  get_vaccine_location_by_vaccine_id,
                                  user_id=user_id,
                                  table_id='vaccine_id'
                                  )
        
        test_data = show_favorites(get_testing_saved_locations, 
                                   get_testing_location_by_test_id,
                                   user_id=user_id, 
                                   table_id='test_id'
                                    )

        symptom_data = show_favorites(get_symptom_tracker_user_id_symptoms,
                                      get_symptom_by_id,
                                      user_id=user_id, 
                                      table_id='symptom_id'
                                      ) 

        data = {
                'vac_data': vac_data, 
                'test_data': test_data, 
                'symptom_data': symptom_data
                }

        return render_template('user_profile.html', user=user, data=data, enumerate=enumerate )

    flash('Sign Up or Log In in order to see your user profile.')
    return redirect('/')