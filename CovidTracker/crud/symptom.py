from CovidTracker.models.model import Symptom
from CovidTracker.connect import db

def create_symptom(symptom):
    """Create and return a symptom(s)"""

    symptom = Symptom(symptom_name=symptom)

    db.session.add(symptom)
    db.session.commit()
    
    return symptom


def get_symptoms():
    """Return all symptoms by id"""
    return Symptom.query.all()


def get_symptom_by_id(symptom_id):
    return Symptom.query.filter_by(symptom_id=symptom_id).first()


def upd_symptom_by_id(symptom_id, symptom):
    symptom_record = get_symptom_by_id(symptom_id)
    symptom_record.symptom_name = symptom
    db.session.commit()


def del_symptom_by_symptom(symptom):
    Symptom.query.filter_by(symptom=symptom).delete()


def del_symptom_by_id(symptom_id):
    Symptom.query.filter_by(symptom_id=symptom_id).delete()
