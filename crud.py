"""CRUD operations"""

from model import db, User, Symptom, SymptomTracker, TestingLocation, VaccineLocation, SavedTestingLocation, SavedVaccineLocation, connect_to_db
def create_user(username, email, password):
    """Create and return a new user."""

    user = User(username=username, email=email, password_hash=password)

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

    tracker = SymptomTracker(symptom_date=symptom_date, user_id=user_id, symptom_id=symptom_id)

    db.session.add(tracker)
    db.session.commit()

    return tracker


def create_saved_locations(user_id, test_id):
    """Create and return a saved location"""

    saved_testing_location = SavedTestingLocation(user_id=user_id, test_id=test_id)

    db.session.add(saved_testing_location)
    db.session.commit()

    return saved_testing_location


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


def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)


# def get_symptoms():
#     """Return all symptoms by id"""

#     return Symptom.query.get(symptom_id)

############
"Question"
##############
# def get_saved_locations():
#     """Return all saved locations"""
#     # have a user in session = you have user_id
#     # a table that relates user_id to all their favorited locations
    
#     saved_locations = get_saved_locations(???)

#     locations = []

#     for location in locations:
#         print()


# def update_user_email(email):
#     """Update the user's email"""
    
#     # Filter for the user that you want to update their email
#     db.session.query(User).filter(User.user_id==user_id).update({"email": email})
#     db.session.commit()


# def update_user_password(password_hash):
#     """Update the user's password"""

#     # Filter for the user that you want to update their email
#     db.session.query(User).filter(User.user_id==user_id).update({"password_hash": password_hash})
#     db.session.commit()


def delete_trackers():
    pass


def delete_saved_locations():
    pass


if __name__ == '__main__':
    from server import app
    connect_to_db(app)