"""CRUD operations"""

from model import db, User, Symptom, Tracker, TestingLocation, VaccineLocation, SavedLocation, connect_to_db


def create_user(username, email, password):
    """Create and return a new user."""

    user = User(username=username, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user.user_id    

def create_symptom(symptom):
    """Create and return a symptom(s)"""

    symptom = Symptom(symptom_name=symptom)

    db.session.add(symptom)
    db.session.commit()

    return symptom


def create_tracker(symptom_date, user_id, symptom_id):
    """Create and return a new symptom tracker"""

    tracker = Tracker(symptom_date=symptom_date, user_id=user_id, symptom_id=symptom_id)

    db.session.add(tracker)
    db.session.commit()

    return tracker


def create_saved_locations(user_id, test_id, vaccine_id):
    """Create and return a saved location"""

    saved_location = SavedLocation(user_id=user_id, test_id=test_id, vaccine_id=vaccine_id)

    db.session.add(saved_location)
    db.session.commit()

    return saved_location


def get_user_by_email(email):
    """Get user by email"""
    
    user = User.query.filter_by(email=email).first()

    if user is None:
        result = {'username': None}
        return result

    else:
        result = {
            'username':user.username,
            'email':user.email,
            'password': user.password,
            'user_id': user.user_id
        }

        return result


def get_user_by_name():
    pass


def get_trackers_symptoms():
    pass


def get_saved_locations():
    pass


def update_user_email(email):
    """Update the user's email"""
    
    # Filter for the user that you want to update their email
    db.session.query(User).filter(User.userid==userid).update({"email": email})
    db.session.commit()


def update_password():
    pass


def delete_trackers():
    pass


def saved_locations():
    pass


if __name__ == '__main__':
    from server import app
    connect_to_db(app)