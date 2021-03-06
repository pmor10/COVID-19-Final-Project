from CovidTracker.models.model import VaccineLocation, SavedVaccineLocation
from CovidTracker.connect import db

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
    return SavedVaccineLocation.query.filter(SavedVaccineLocation.user_id == user_id).all()


def check_vaccine_saved_location_in_favorites(user_id, vaccine_id):

    return SavedVaccineLocation.query.filter(SavedVaccineLocation.user_id == user_id, SavedVaccineLocation.vaccine_id == vaccine_id).first()


def del_vaccine_saved_locations(user_id, vaccine_id):
    
    SavedVaccineLocation.query.filter(SavedVaccineLocation.user_id == user_id, SavedVaccineLocation.vaccine_id == vaccine_id).delete()

    db.session.commit()