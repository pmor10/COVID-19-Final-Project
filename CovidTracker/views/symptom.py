from CovidTracker.app import app 
from CovidTracker.crud.symptom import get_symptoms
from CovidTracker.crud.tracker import create_symptom_tracker, get_symptom_tracker_user_id_symptoms

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
            if datetime.datetime.date(today) == datetime.datetime.date(symptom.symptom_date):
                symptom_count += 1
        
        if symptom_count >= 3:
            msg = 'Please visit your local doctor for a checkup.'

        symptoms = request.form.items()
        
        added_symptoms=[]

        if symptoms:
            for k,v in symptoms:
                try:
                    tracker = create_symptom_tracker(user_id, k)
                    added_symptoms.append(v)
                except:
                    pass 
            
            msg = f'The following symptoms were added to profile: {added_symptoms}'

    else:
        msg = 'Please Login'
        flash(msg)
    return jsonify(msg)
