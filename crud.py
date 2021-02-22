"""CRUD operations"""

from model import db, User, Symptom, SymptomTracker, TestingLocation, VaccineLocation, SavedTestingLocation, SavedVaccineLocation, connect_to_db
from datetime import datetime


def create_user(username, email, password, salt):
    """Create and return a new user."""

    user = User(username=username, email=email, password=password, salt=salt)

    db.session.add(user)
    db.session.commit()

    return user.user_id    


def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.filter_by(user_id=user_id).first()


def get_user_by_username(username):
    """This returns the username value from the database."""
    return User.query.filter_by(username=username).first()


def get_user_by_email(email):
    """Get user by email"""
    
    return User.query.filter_by(email=email).first()

def upd_user_email_by_email(email, new_email):
    user = get_user_by_email(email)
    user.email = new_email
    db.session.commit() 
    

def upd_user_email_by_id(user_id, new_email):
    user = get_user_by_id(user_id)
    user.email = new_email
    db.session.commit()


def upd_user_password(user_id, old_password, new_password):
    user = get_user_by_id(user_id)

    if old_password == _get_user_password(user_id):
        user.password = new_password 
        db.session.commit() 


def _get_user_password(user_id):
    user = get_user_by_id(user_id)
    return user.password


def create_symptom(symptom):
    """Create and return a symptom(s)"""

    symptom = Symptom(symptom_name=symptom)

    db.session.add(symptom)
    db.session.commit()
    
    return symptom


def get_symptoms():
    """Return all symptoms by id"""
    return Symptom.query.all()


def get_symptom_by_id(symptom_id):
    return Symptom.query.filter_by(symptom_id=symptom_id).first()


def upd_symptom_by_id(symptom_id, symptom):
    symptom_record = get_symptom_by_id(symptom_id)
    symptom_record.symptom_name = symptom
    db.session.commit()


def del_symptom_by_symptom(symptom):
    Symptom.query.filter_by(symptom=symptom).delete()


def del_symptom_by_id(symptom_id):
    Symptom.query.filter_by(symptom_id=symptom_id).delete()


#================== Symptom Tracker Section =====================#
def create_symptom_tracker(user_id, symptom_id, symptom_date=None):
    """Create and return a new symptom tracker"""

    if not symptom_date:
        symptom_date = datetime.today()
    tracker = SymptomTracker(user_id=user_id, symptom_id=symptom_id, symptom_date=symptom_date)

    db.session.add(tracker)
    db.session.commit()
    
    
    return tracker


def get_symptom_tracker_user_id_symptoms(user_id):

    return SymptomTracker.query.filter_by(user_id=user_id).all()


def del_symptom_tracker(user_id, symptom_id):

    SymptomTracker.query.filter(SymptomTracker.symptom_id==symptom_id, SymptomTracker.user_id==user_id).delete()


#=================== Testing Location ========================# 
def get_testing_location_by_zipcode(zip_code):

    return TestingLocation.query.filter_by(zip_code=zip_code).all()

def get_testing_location_by_test_id(test_id):

    return TestingLocation.query.filter_by(test_id=test_id).first()


def create_testing_saved_locations(user_id, test_id):
    """Create and return a saved location"""

    saved_testing_location = SavedTestingLocation(user_id=user_id, test_id=test_id)

    db.session.add(saved_testing_location)
    db.session.commit()
    
    return saved_testing_location


def get_testing_saved_locations(user_id):

    return SavedTestingLocation.query.filter(SavedTestingLocation.user_id==user_id).all()

def check_testing_saved_location_in_favorites(user_id, test_id):

    return SavedTestingLocation.query.filter(SavedTestingLocation.user_id==user_id, SavedTestingLocation.test_id==test_id).first()


def del_testing_saved_locations(user_id, test_id):

    return SavedTestingLocation.query.filter(SavedTestingLocation.user_id==user_id, SavedTestingLocation.test_id==test_id).delete()


#======================== Vaccine Location ======================# 
def get_vaccine_location_by_zipcode(zip_code):

    return VaccineLocation.query.filter_by(zip_code=zip_code).all()


def get_vaccine_location_by_vaccine_id(vaccine_id):

    return VaccineLocation.query.filter_by(vaccine_id=vaccine_id).first()


def create_vaccine_saved_locations(user_id, vaccine_id):
    """Create and return a saved location"""

    saved_vaccine_location = SavedVaccineLocation(user_id=user_id, vaccine_id=vaccine_id)

    db.session.add(saved_vaccine_location)
    db.session.commit()
    
    return saved_vaccine_location


def get_vaccine_saved_locations(user_id):
    return SavedVaccineLocation.query.filter(SavedVaccineLocation.user_id==user_id).all()


def check_vaccine_saved_location_in_favorites(user_id, vaccine_id):

    return SavedVaccineLocation.query.filter(SavedVaccineLocation.user_id==user_id, SavedVaccineLocation.vaccine_id==vaccine_id).first()    


def del_vaccine_saved_locations(user_id, vaccine_id):
    return SavedVaccineLocation.query.filter(SavedVaccineLocation.user_id==user_id, SavedVaccineLocation.vaccine_id==vaccine_id).delete()



if __name__ == '__main__':
    from server import app
    connect_to_db(app)