from CovidTracker.config import TEMPLATES_DIR, STATIC_DIR 
from CovidTracker.connect import db 
from flask import (Flask)


# Points to the directories for templates and static in the config file

app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)
app.secret_key = "dev"

# import needs to occur after Flask app is instantiated. 
from CovidTracker.views.index import * 
from CovidTracker.views.login import *
from CovidTracker.views.logout import *
from CovidTracker.views.profile import *
from CovidTracker.views.signup import *
from CovidTracker.views.symptom import *
from CovidTracker.views.testing import *
from CovidTracker.views.vaccine import * 