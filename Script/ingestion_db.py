import pandas as pd 
import os 
from sqlalchemy import create_engine
import logging
import time

logging.basicConfig(
    filename = "logs/ingestion_db.log",
    level = logging.DEBUG,
    format = "%(asctime)s - %(levelname)s - %(message)s",
    filemode = "a"
)

engine = create_engine("sqlite:///inventory.db")
def ingest_db(df, table_name, engine):
    ''' this function will ingest dataframe into database table'''
    df.to_sql(table_name, con = engine, if_exists = 'replace', index = False)

def load_raw_data(folder):
    ''' this function is load the csv as dataframe and ingest into db'''
    start = time.time()
    for file in os.listdir(folder):
        if file.endswith('.csv'):
           path = os.path.join(folder, file)
           df = pd.read_csv(path)
           logging.info(f'ingesting {file} in db')
           ingest_db(df,file[:-4], engine)
         
        end = time.time()
        total_time = (end - start)/60
        logging.info('-------ingestion complete---------')
        
        logging.info(f'total time taken:{total_time} minutes')

if __name__ == "__main__":
    folder =   r"C:\Users\pranj\Downloads\data\data" 
    ingestion_db.load_raw_data(folder)