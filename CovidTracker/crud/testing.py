from CovidTracker.models.model import TestingLocation, SavedTestingLocation
from CovidTracker.connect import db

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

    SavedTestingLocation.query.filter(SavedTestingLocation.user_id==user_id, SavedTestingLocation.test_id==test_id).delete()

    db.session.commit()