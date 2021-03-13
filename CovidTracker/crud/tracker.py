from CovidTracker.models.model import SymptomTracker
from CovidTracker.connect import db
import datetime

def create_symptom_tracker(user_id, symptom_id, symptom_date=None):
    """Create and return a new symptom tracker"""

    if not symptom_date:
        today = datetime.datetime.today()
        symptom_date = datetime.datetime.date(today)
    tracker = SymptomTracker(user_id=user_id, symptom_id=symptom_id, symptom_date=symptom_date)

    db.session.add(tracker)
    db.session.commit()
    
    return tracker


def get_symptom_tracker_user_id_symptoms(user_id):

    user_symptoms =  SymptomTracker.query.filter_by(user_id=user_id).all()
    
    return user_symptoms


def del_symptom_tracker(user_id, symptom_id, symptom_date):
    
    d = SymptomTracker.query.filter(SymptomTracker.symptom_id==symptom_id, SymptomTracker.user_id==user_id, SymptomTracker.symptom_date==symptom_date).delete()
    print('D'*7777, user_id, symptom_id, symptom_date, d)
    db.session.commit()

