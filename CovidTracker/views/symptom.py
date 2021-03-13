from CovidTracker.app import app 
from CovidTracker.crud.symptom import get_symptoms, get_symptom_by_id
from CovidTracker.crud.tracker import create_symptom_tracker, get_symptom_tracker_user_id_symptoms, del_symptom_tracker
import json 
import datetime 

from flask import (render_template, request, session, flash, jsonify)

@app.route('/symptoms')
def symptom_tracker():
    symptoms = get_symptoms()
    two_col_symptoms = tuple(zip(symptoms[1::2], symptoms[::2]))

    return render_template('symptoms.html', symptoms=symptoms, two_col_symptoms=two_col_symptoms)

@app.route('/add_symptoms', methods=['GET', 'POST'])
def add_symptoms():


    if 'user_id' in session:
        user_id = session['user_id']
        msg = "User logged in"
        today = datetime.datetime.now()
        user_symptoms = get_symptom_tracker_user_id_symptoms(user_id)
        
        symptom_count = 0
        for symptom in user_symptoms:
            if datetime.datetime.date(today) == symptom.symptom_date:
                symptom_count += 1
        
        if symptom_count >= 3:
            msg = 'Please visit your local doctor for a checkup.'

        data = request.get_data()
        symptoms = json.loads(data.decode('utf-8'))['data']
        
        added_symptoms=[]
        
        if symptoms:
            for k in symptoms:
                symptom_id = int(k)
                user_symptoms = [symptom.symptom_id for symptom in get_symptom_tracker_user_id_symptoms(user_id)]
                
                if symptom_id not in user_symptoms:

                    tracker = create_symptom_tracker(user_id, symptom_id)
                    added_symptoms.append(get_symptom_by_id(symptom_id).symptom_name)

            msg = {'added_symptoms': added_symptoms}

    else:
        msg = 'Please Login'
        flash(msg)
    return jsonify(msg)


@app.route('/delete_symptom', methods=['POST'])
def delete_symptom():
    """ Delete testing location from the database """

    user_id = session.get('user_id', None)
    data = request.get_data();

    myjson = json.loads(data.decode('utf-8').replace("'", '"'))
    
    symptom_id = myjson['symptom_id']
    symptom_date = myjson['symptom_date']
    
    del_symptom_tracker(user_id, symptom_id, symptom_date)
    
    flash("Location removed!")

    return jsonify("Success!")