from CovidTracker.models.model import User
from CovidTracker.connect import db

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