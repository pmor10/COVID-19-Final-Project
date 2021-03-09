from CovidTracker.models.model import Covid
from CovidTracker.connect import db

def get_current_covid_data():


    covid = Covid.query.order_by(Covid.date.desc()).limit(1).first()
    
    return covid
