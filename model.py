"""Models for Covid-19 California's Locations and Symptoms Tracker."""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from setting import DB_INFO


db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fullname = db.Column(db.String(50), nullable= False)
    username = db.Column(db.String(256), unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(120), nullable=False)
    
    tracker = db.relationship("Tracker", backref="users")
    saved_location = db.relationship("SavedLocation", backref="users")

    
    def __repr__(self):
        return f'<User user_id={self.user_id} username={self.username} email={self.email}>'


class Symptom(db.Model):
    """A symptom."""

    __tablename__ = 'symptoms'

    symptom_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    symptom_name = db.Column(db.String(120))

    tracker = db.relationship("Tracker", backref="symptoms")


    def __repr__(self):
        return f'<Symptom symptom_name={self.symptom_name} severity={self.severity}>'
        

class Tracker(db.Model):
    """A symptom tracker."""

    __tablename__ = 'trackers'

    tracker_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    symptom_id = db.Column(db.Integer, db.ForeignKey('symptoms.symptom_id'))
    symptom_date = db.Column(db.DateTime)


    def __repr__(self):
        return f'<Tracker tracker_id={self.tracker_id} user_id={self.user_id} symptom_id={self.symptom_id}>'    


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

    saved_location = db.relationship("SavedLocation", backref="test_locations")


    def __repr__(self):
        return'<Testing Location organization_id={self.organization_id} alternate_name={self.alternate_name} address={self.address}>' 


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

    saved_location = db.relationship("SavedLocation", backref="vaccine_locations")


    def __repr__(self):
        return'<Vaccine Location name={self.name} zip_code={self.zip_code} vaccine_id={self.vaccine_id}>'


class SavedLocation(db.Model):
    """A Saved Location."""

    __tablename__ = 'saved_locations'
    
    location_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    test_id = db.Column(db.Integer, db.ForeignKey('test_locations.test_id'))
    vaccine_id = db.Column(db.Integer, db.ForeignKey('vaccine_locations.vaccine_id'))


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