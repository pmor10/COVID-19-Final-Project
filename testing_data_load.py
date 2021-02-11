import pandas as pd
import json
import numpy as np
import requests

from sqlalchemy import engine
from setting import DB_INFO

# Pull the json from here
url = 'https://covid-19-testing.github.io/locations/california/complete.json'

# Get the json data
r = requests.get(url).json()

# Access the key and values for dataframe

# Load json data into dataframe
data = []

for i in range(len(r)):    
    
    physical_address =  r[i]['physical_address'][0]
    phone_numbers = r[i]['phones'][0]
    
    org_id = r[i]['organization_id']
    alt_name = r[i]['alternate_name']
    descr = r[i]['description']
    transport = r[i]['transportation']
    address = physical_address['address_1']
    region = physical_address['region']
    state_province = physical_address['state_province']
    postal_code = physical_address['postal_code']
    country = physical_address['country']
    phone = phone_numbers['number']
    city = physical_address['city']
    

    data.append((org_id, alt_name, descr, transport, address, 
                region, state_province, postal_code, country,
                phone, city))
    
test_columns = ['organization_id', 'alternate_name', 'description', 'transportation', 
                'address', 'region', 'state_province', 'zip_code', 'country', 'phone_number',
                'city']
    
df_test = pd.DataFrame(data)
df_test.columns = test_columns 

con = engine.create_engine(DB_INFO)

with con.connect() as conn: 
    conn.execute('truncate table test_locations restart identity cascade;')

df_test.to_sql('test_locations', con=con, schema='public', index=False, if_exists='append')