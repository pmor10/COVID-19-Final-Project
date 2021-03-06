"""Models for Covid-19 California's Locations and Symptoms Tracker."""

from flask_sqlalchemy import SQLAlchemy
from CovidTracker.config import DB_INFO
from flask_login import UserMixin
from CovidTracker.connect import db, connect_to_db 


class Covid(db.Model):
    """Covid Cases Data"""

    __tablename__ = 'covid_cases'

    date = db.Column(db.String(10), primary_key=True)
    death = db.Column(db.DECIMAL(22,7))
    positive = db.Column(db.DECIMAL(22,7))
    totalTestResults = db.Column(db.DECIMAL(22,7))
    hospitalizedCurrently = db.Column(db.DECIMAL(22,7))

    def __repr__(self):
        return f'<Covid date={self.date} death={self.death} positive={self.positive} total_test_results={self.totalTestResults} hospitalized_currently={self.hospitalizedCurrently}>'

class User(UserMixin, db.Model):
    """A user."""
    
    def get_id(self):
        return self.user_id
        
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(256), unique=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(120), nullable=False)
    salt = db.Column(db.String(300), nullable=False)
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
        return f'<Symptom symptom_name={self.symptom_name} symptom_id={self.symptom_id} >'
    

class SymptomTracker(db.Model):
    """A symptom tracker."""

    __tablename__ = 'symptom_tracker'

    #tracker_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    symptom_id = db.Column(db.Integer, db.ForeignKey('symptoms.symptom_id'), primary_key=True)
    symptom_date = db.Column(db.Date, primary_key=True)


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
        return'<Testing Location test_id={self.test_id} organization_id={self.organization_id} alternate_name={self.alternate_name} address={self.address} state={self.state_province} zip_code={self.zip_code} city={self.city} phone_number={self.phone_number}>' 


class SavedTestingLocation(db.Model):
    """A Saved Location."""

    __tablename__ = 'saved_testing_locations'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('test_locations.test_id'), primary_key=True)


    def __repr__(self):
        return '<Saved Location test_id={self.test_id}  user_id={self.user_id}>'


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
        return'<Vaccine Location name={self.name} Location address={self.address} state={self.state} zip_code={self.zip_code} vaccine_id={self.vaccine_id} latitude={self.latitude}> longitude={self.longitude}'


class SavedVaccineLocation(db.Model):
    """A Saved Location."""

    __tablename__ = 'saved_vaccine_locations'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    vaccine_id = db.Column(db.Integer, db.ForeignKey('vaccine_locations.vaccine_id'), primary_key=True)


    def __repr__(self):
        return '<Saved vaccine_id={self.vaccine_id} user_id={self.user_id}>'

recreate_db = connect_to_db