import os
from random import choice, randint

import crud
import model
import server 

# os.system('dropdb postgres')
# os.system('createdb postgres')

model.connect_to_db(server.app)
model.db.create_all()

symptoms = ['chills', 
            'headache', 
            'congestion', 
            'nausea', 
            'fatigue', 
            'fever', 
            'shortness_breath',
            'cough', 
            'sore_throat']

for s in symptoms:
    crud.create_symptom(s)


# create 10 dummy users
for n in range(10):

    username = f'user{n}'
    email = f'user{n}@test.com'
    password = 'test'

    crud.create_user(username, email, password)

# import testing_data_load
# import vaccine_data_load
