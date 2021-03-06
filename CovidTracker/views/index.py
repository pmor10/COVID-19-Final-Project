from CovidTracker.app import app 
from CovidTracker.crud.covid_data import get_current_covid_data

from flask import (render_template)

import datetime

@app.route('/')
def index():
    """Display Landing Page"""

    now = datetime.datetime.now().strftime('%B %d, %Y')
    year = datetime.datetime.now().strftime('%Y')
    month = datetime.datetime.now().strftime('%B, %d')

    covid_cases = get_current_covid_data()
    death = "{:,.0f}".format(covid_cases.death)
    positive = "{:,.0f}".format(covid_cases.positive)
    hospitalized = "{:,.0f}".format(covid_cases.hospitalizedCurrently)
    totaltestresults = "{:,.0f}".format(covid_cases.totalTestResults)

    return render_template('index.html', now=now,  month=month, year=year, death=death, positive=positive, hospitalizedCurrently=hospitalized, totalTestResults=totaltestresults)