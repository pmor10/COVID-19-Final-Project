"""Models for Covid-19 California's Locations and Symptoms Tracker."""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from setting import DB_INFO
from flask_login import UserMixin


db = SQLAlchemy()

class User(UserMixin, db.Model):
    """A user."""
    
    def get_id(self):
        return self.user_id
        
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(256), unique=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(120), nullable=False)
    
    tracker = db.relationship("Symptom", secondary='symptom_tracker')
    
    saved_vaccine_location = db.relationship("SavedVaccineLocation", backref='user')
    saved_testing_location = db.relationship("SavedTestingLocation", backref='user')

    def __repr__(self):
        return f'<User user_id={self.user_id} username={self.username} email={self.email}>'


class Symptom(db.Model):
    """A symptom."""

    __tablename__ = 'symptoms' 

    symptom_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    symptom_name = db.Column(db.String(100))

    tracker = db.relationship("User", secondary='symptom_tracker')


    def __repr__(self):
        return f'<Symptom symptom_name={self.symptom_name}>'
    

class SymptomTracker(db.Model):
    """A symptom tracker."""

    __tablename__ = 'symptom_tracker'

    #tracker_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    symptom_id = db.Column(db.Integer, db.ForeignKey('symptoms.symptom_id'), primary_key=True)
    symptom_date = db.Column(db.DateTime)


    user = db.relationship('User', backref=db.backref('saved_symptom'))
    symptom = db.relationship('Symptom', backref=db.backref('saved_user'))


    def __repr__(self):
        return f'<SymptomTracker user_id={self.user_id} symptom_id={self.symptom_id} symptom_date={self.symptom_date} symptom_name={self.symptom.symptom_name}>'    


class TestingLocation(db.Model):
    """A Testing Location."""

    __tablename__ = 'test_locations'

    test_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    organization_id = db.Column(db.Integer)
    alternate_name = db.Column(db.String(120))
    description = db.Column(db.String)
    transportation = db.Column(db.String(120))
    address = db.Column(db.String(120))
    region = db.Column(db.String(35))
    state_province = db.Column(db.String(3))
    zip_code = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String(2))
    phone_number = db.Column(db.String(20))
    city = db.Column(db.String(100))


    def __repr__(self):
        return'<Testing Location organization_id={self.organization_id} alternate_name={self.alternate_name} address={self.address}>' 


class SavedTestingLocation(db.Model):
    """A Saved Location."""

    __tablename__ = 'saved_testing_locations'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('test_locations.test_id'), primary_key=True)


    def __repr__(self):
        return '<Saved Location location_id={self.location_id} vaccine_id={self.vaccine_id} user_id={self.user_id}>'


class VaccineLocation(db.Model):
    """A Vaccine Location."""

    __tablename__ = 'vaccine_locations'

    vaccine_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    address = db.Column(db.String(500))
    latitude = db.Column(db.Numeric, nullable=False)
    longitude = db.Column(db.Numeric, nullable=False)
    location_type = db.Column(db.String(200))
    name = db.Column(db.String(200), nullable=False)
    state = db.Column(db.String(100))
    zip_code = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return'<Vaccine Location name={self.name} zip_code={self.zip_code} vaccine_id={self.vaccine_id}>'


class SavedVaccineLocation(db.Model):
    """A Saved Location."""

    __tablename__ = 'saved_vaccine_locations'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    vaccine_id = db.Column(db.Integer, db.ForeignKey('vaccine_locations.vaccine_id'), primary_key=True)


    def __repr__(self):
        return '<Saved Location location_id={self.location_id} vaccine_id={self.vaccine_id} user_id={self.user_id}>'


def connect_to_db(flask_app, db_uri=DB_INFO, echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')

    with flask_app.app_context():
        db.create_all()

if __name__ == '__main__':
    from server import app

    connect_to_db(app)