import requests
from sqlalchemy import create_engine
import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy_utils import database_exists, create_database
import logging

logging.basicConfig(filename='number_ex2.txt', level=logging.INFO)
log = logging.getLogger()
url = 'https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films'
log.info(f"Fetching data from URL: {url}")
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
#alltables = soup.find_all('tbody')
tables = pd.read_html(str(soup))
log.info(f"Number of tables found: {len(tables)}")

table1 = tables[0]
table2 = tables[1]
table3 = tables[2]
log.info(f"Tables extracted successfully")

log.info("Merging table1 and table2.")
merged_df = pd.merge(table1, table2, how='inner', left_on='Average Rank', right_on='Occurrences')  
log.info(f"Tables merged successfully")

merged_df = merged_df.head(17)
log.info("Limiting the result to the first 17 rows.")

#df = merged_df.DataFrame(columns=['Average Rank',	'Film',	'Year',	'Rotten Tomatoes Top 100',	'IMDb Top 250',	'Empire Top 100',	'AFI Top 100',	'BFI Top 100','Rank',	'Decade',	'Occurrences'])
log.info(f"Result: {merged_df}")

uid = 'postgres'
pwd = ''  # put in your password
postgres_url = f'postgresql+psycopg2://{uid}:{pwd}@localhost:5432/best_films'

if not database_exists(postgres_url):
    create_database(postgres_url)
    log.info('Database created.')
else:
    log.info('database exists')

engine = create_engine(postgres_url)

first_second_table = 'first_second'
csv_path = 'firts_second_table.csv'

merged_df.to_sql(first_second_table, engine, if_exists='replace')  # Transfer the data to the database
log.info(f'Successfully transferred data to the database table {first_second_table}.')
print('Successfully transferred to the database')

merged_df.to_csv(csv_path)  # Save the data to a CSV file
log.info(f'Successfully saved data to CSV file: {csv_path}.')


re_table1 = table1.iloc[:, :3]  # Extract the first three columns
log.info("Extracting 'Genre' from the second table.")
genre_table = table3[['Genre']]# Extract the 'Genre' column from the third table

re_table1.insert(1, 'Number', range(1, len(table1) + 1)) # Insert a new column 'Number' at index 1
 
second_merged_df = pd.concat([re_table1, genre_table], axis = 1)  
re_merged_df = merged_df.head(17)
log.info(f"Result: {re_merged_df}")
    
uid = 'postgres'
pwd = '07063902274'
postgres_url2 = f'postgresql+psycopg2://{uid}:{pwd}@localhost:5432/best_films'

if not database_exists(postgres_url2):
    create_database(postgres_url2)
    log.info('Database created.')
else:
    log.info('database exists')

engine = create_engine(postgres_url2)

first_third_table = 'first_third'
csv_path2 = 'first_third_table.csv'

re_merged_df.to_sql(first_third_table, engine, if_exists='replace')  # Transfer the data to the database
log.info(f'Successfully transferred data to the database table {first_third_table}.')
print('Successfully transferred to the database')

re_merged_df.to_csv(csv_path2)  # Save the data to a CSV file
log.info(f'Successfully saved data to CSV file: {csv_path2}.')
