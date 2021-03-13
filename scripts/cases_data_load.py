import pandas as pd
import numpy as np
import requests
import sys 
sys.path.append('..')
from CovidTracker.config import DB_INFO
from sqlalchemy.engine import create_engine
from io import StringIO

url = 'https://covidtracking.com/data/download/california-history.csv'

# Get the json data
r = requests.get(url)

data = StringIO()

data.write(r.content.decode())

data.seek(0)

cur = create_engine(DB_INFO)

df = pd.read_csv (data)

df2 = df[['date', 'death', 'positive', 'totalTestResults', 'hospitalizedCurrently']].fillna(0)

df2.to_sql('covid_cases', con=cur, schema='public', index=False, if_exists='replace')

