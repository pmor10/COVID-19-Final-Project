import os
from random import choice, randint
from CovidTracker.app import app 
from CovidTracker.connect import connect_to_db, db 
from CovidTracker.crud.symptom import create_symptom
from CovidTracker.models.model import recreate_db
# os.system('sudo -u postgres dropdb postgres')
# os.system('sudo -u postgres createdb postgres')

recreate_db(app)

symptoms = ['Chills', 
            'Congestion or runny nose', 
            'Cough', 
            'Diarrhea', 
            'Fatigue', 
            'Fever', 
            'Headache', 
            'Muscle or body aches',
            'Nausea or vomiting',
            'New loss of taste or smell',
            'Shortness of breath or difficulty breathing',
            'Sore throat']

for s in symptoms:
    create_symptom(s)
