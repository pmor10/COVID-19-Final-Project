import pandas as pd
import json
import numpy as np
import requests
import sys 
sys.path.append('..')
from sqlalchemy import engine
from CovidTracker.config import DB_INFO

# Pull the json from here
url = 'https://api.vaccinateca.com/v1/locations.json'

# Get the json data
r = requests.get(url).json()

# Access the key and values for dataframe
data = r['content']

# Load json data into dataframe
df = pd.DataFrame(data)

# Data cleaning steps
addr = df['Address'].str.split(',',n=1, expand=True)[1]
zip_code = addr.str.extract(r'(\d+)', expand= False)
df['Zip Code'] = zip_code
df['State'] = 'CA'

# Selecting columns for database
use_cols = ['Address', 'Latitude', 'Longitude', 'Location Type', 'Name', 'State', 'Zip Code']
df = df[use_cols] 

df['Name'] = df['Name'].str.split('(', expand=True)[0].str.strip()
df['Name'] = df['Name'].str.split('#', expand=True)[0].str.strip()
df['Name'] = df['Name'].str.split('(at){1}', expand=True)[0].str.strip()
df['Name'] = df['Name'].str.rstrip('012345679').str.strip().str.title()

# Creating database connection
con = engine.create_engine(DB_INFO)

# Overwriting column names in dataframe to match database column names (must match)
db_col_names = ['address', 'latitude', 'longitude', 'location_type', 'name', 'state', 'zip_code']
df.columns = db_col_names

# Drop all rows with an empty zipcode. This means that there was no address provided. Not helpful!
df = df[~df['zip_code'].isnull()]

# Reading data from database
df_db = pd.read_sql('SELECT * FROM vaccine_locations', con)

# Union and drop duplicates
df = pd.concat([df_db.iloc[:, 1:], df]).drop_duplicates(keep=False, subset=['latitude', 'longitude'])

# connection exexcute 
df.to_sql('vaccine_locations', con, 'public', index=False, if_exists='append')