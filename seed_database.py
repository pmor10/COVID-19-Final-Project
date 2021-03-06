import os
from random import choice, randint
from CovidTracker.app import app 
from CovidTracker.connect import connect_to_db, db 
from CovidTracker.crud.symptom import create_symptom, get_symptoms, del_symptom_tracker, get_symptom_tracker, get_symptom_by_id

os.system('sudo -u postgres dropdb postgres')
os.system('sudo -u postgres createdb postgres')

connect_to_db(app)
db.create_all()

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


# create 10 dummy users
# for n in range(10):

#     username = f'user{n}'
#     email = f'user{n}@test.com'
#     password = 'test'

#     crud.create_user(username, email, password)

# import testing_data_load
# import vaccine_data_load



print(get_symptoms())

for user, symptom in [(1,1), (1,2), (1,3), (2,1), (2,4)]:

    create_symptom_tracker(user, symptom)

records = get_symptom_tracker(1)

for record in records:
    print(record.symptom.symptom_name, record.user.username)

d = del_symptom_tracker(1, 1)

records1 = get_symptom_tracker(1)
for record in records1:
    print(record.symptom.symptom_name, record.user.username)

s1 = get_symptom_by_id(1)
print(s1)

# u1 = crud.upd_symptom_by_id(1, 'Hairloss')
# print(crud.get_symptom_by_id(1))


# crud.create_user('pari', 'pari_morton@email.com', 'CuddlesTheCatIsCool')

# pari = crud.get_user_by_email('pari_morton@email.com')
# print(pari)
# crud.upd_user_password(11, 'CuddlesTheCatIsCool', 'ButJasmineIsTheBestest')

# pari = crud.get_user_by_id(11)
# print(pari)

# print(crud._get_user_password(11))