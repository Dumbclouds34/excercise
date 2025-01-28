import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import os

# Load the CSV file
data_path = os.chdir(r'C:\Users\GIVEN\Documents')
df = pd.read_csv('RewardsData.csv')

f = pd.DataFrame(df, index=range(1, len(df)+1))
new_df = df.drop(columns ='Tags')

new_df['City'] = new_df['City'].apply(str)
alpha_order =new_df['City'].unique()
alpha_order.sort()
#print(alpha_order)

new_df['City'].replace(to_replace= ['Winston Salem', 'Winston Salem', 'Winston salem',
 'Winston salem', 'Winston-Salem', 'Winston-Salem',
 'Winston-Salem','Winston-salem', 'winston salem', 'winston salem'], value='Winston-Salem', inplace= True)
new_df['City'] = new_df['City'].str.title()
#print(new_df['City'])

new_df['State'] = new_df['State'].apply(str)
beta_order = new_df['State'].unique()
beta_order.sort()

us_cities = {
    'AL': 'Alabama', 'Al': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming',
}
new_df['State'] = new_df['State'].map(us_cities)
print(new_df.head())


us_states = [
    'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 
    'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 
    'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 
    'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 
    'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 
    'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 
    'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 
    'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 
    'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 
    'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
]
empty_cells = new_df[new_df['State'] == ''].index
print(f"Empty cells indices: {empty_cells}")
state_index = 0
for i in empty_cells:
    new_df.loc[i, 'State'] = us_states[state_index]
    state_index = (state_index + 1) % len(us_states)  # Cycle through the list


df['Zip'] = df['Zip'].astype(str).str[:5] # Extract the first 5 digits of the ZIP code


df = df[df['Zip'].str.len() == 5] # Keep only rows with ZIP codes of length 5


df['Birthdate'] = pd.to_datetime(df['Birthdate'], errors='coerce').dt.date # Convert the 'Birthdate' column to datetime


uid = 'postgres'
pwd = '' #put in your password
postgres_url = f'postgresql+psycopg2://{uid}:{pwd}@localhost:5432/PandasData'

engine = create_engine(postgres_url)

if not database_exists(postgres_url):
    create_database(postgres_url)

table = 'New_Data'
df.to_sql(table, con=engine, if_exists='replace', index=False)

print(f"Data sent to '{postgres_url}' , at'{table}' table !")
