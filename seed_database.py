import os
from random import choice, randint

import crud
import model


model.connect_to_db(server.app)
model.db.create_all()

def add_symptom(symptom):

    symptom_obj = crud.create_symptom(symptom)

    db.session.add(symptom_obj)
    db.session.commit()

    return symptom_obj


symptoms = ['chills', 
            'headache', 
            'congestion', 
            'nausea', 
            'fatigue', 
            'fever', 
            'shortness_breath',
            'cough', 
            'sore_throat']

for sympt in symptoms:
    add_symptom(symptom)



# create 10 dummy users
for n in range(10):

    username = f'user{n}'
    email = f'user{n}@test.com'
    password = 'test'

    user = crud.create_user(username, email, password)

