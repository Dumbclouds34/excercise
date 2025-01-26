import requests
from sqlalchemy import create_engine
import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy_utils import database_exists, create_database
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger()

uid = 'postgres'
pwd = '07063902274'
postgres_url = f'postgresql+psycopg2://{uid}:{pwd}@localhost:5432/Banks'

if not database_exists(postgres_url):
    create_database(postgres_url)
    log.info('Database created.')
else:
    log.info('database exists')

engine = create_engine(postgres_url)


url = ' https://web.archive.org/web/20230908091635 /https://en.wikipedia.org/wiki/List_of_largest_banks'

table_name = 'top_17_banks'
csv_path = 'top_17_banks.csv'
df = pd.DataFrame(columns = ['Bank Name','Euro', 'Pound', 'INR'])
count = 0

hmtl_page = requests.get(url).text
retrieved_data = BeautifulSoup(hmtl_page, 'html.parser')
log.info('Successfully retrieved the webpage.')

tables = retrieved_data.find_all('tbody')
rows = tables[0].find_all('tr')


USD_to_EUR = 0.93
USD_to_GBP = 0.8  
USD_to_INR = 82.95
for row in rows:
    if count < 17:  # count starts at 0 and will stop at 16 (indexing)
        col = row.find_all('td')
        if len(col) != 0:  # if the columns are not empty

            
            bank_name = col[1].text
            dollar_text = col[2].text.strip()  
            dollar_value = float(dollar_text) # Convert the parsed content to float

           
            Euro = dollar_value * USD_to_EUR
            Pound = dollar_value * USD_to_GBP
            INR = dollar_value * USD_to_INR

    
            data_dict = {
                'Bank Name' : bank_name,
                'Euro': Euro,
                'Pound': Pound,
                'INR': INR
            }

    
            df1 = pd.DataFrame(data_dict, index=[0])
            df = pd.concat([df, df1], ignore_index=True)

            log.info(f"Processed row {count}: {bank_name}, {dollar_value} USD")
        count += 1  

    else:
        log.info("Processed the top 17 rows. Stopping.")
        break

df.to_sql(table_name, engine, if_exists='replace')  # Transfer the data to the database
log.info(f'Successfully transferred data to the database table {table_name}.')
print('Successfully transferred to the database')
df.to_csv(csv_path)  # Save the data to a CSV file
log.info(f'Successfully saved data to CSV file: {csv_path}.')