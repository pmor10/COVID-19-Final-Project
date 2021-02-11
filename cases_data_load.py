import pandas as pd
import json
import numpy as np
import requests

from sqlalchemy import engine
from setting import DB_INFO

# Pull the json from here
url = 'https://covid-api.mmediagroup.fr/v1/cases'

# Get the json data
r = requests.get(url).json()

states = r['US'].keys()

for k,v in r['US']['California'].items():
    print(k, v)