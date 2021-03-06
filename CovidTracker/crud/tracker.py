from CovidTracker.models.model import SymptomTracker
from CovidTracker.connect import db
from datetime import datetime 

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

