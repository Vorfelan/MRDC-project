import yaml
from sqlalchemy import create_engine, inspect
from sqlalchemy.engine.base import Engine
import pandas as pd

class DatabaseConnector:
    def __init__(self, credentials_path: str):
        self.credentials_path = credentials_path

    def get_credentials(self) -> dict:
        '''
        Loads SQL credentials from YAML file and returns as dictionary.
        '''
        with open(self.credentials_path, 'r') as file:
            credentials = yaml.safe_load(file)
        return credentials
    
    def init_db_engine(self) -> Engine:
        '''
        Intialises and returns an SQLAlchemy engine using the credentials.
        '''
        creds = self.get_credentials()
        engine = create_engine(f"postgresql://{creds['USER']}:{creds['PASSWORD']}@{creds['HOST']}:{creds['PORT']}/{creds['DATABASE']}")
        return engine
    
    def list_db_tables(self) -> list:
        '''
        Lists all tables in database.
        '''
        engine = self.init_db_engine()
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        return tables
    
    def upload_to_db(self, dataframe: pd.DataFrame, table_name: str, if_exists: str = 'fail'):
        '''
        Uploads a DataFrame to a table in the database.
        
        Args:
            dataframe (pd.DataFrame): the DataFrame to upload
            table_name (str): name of table to upload to
            if_exists (str): what to do if table already exists. Options are 'fail', 'replace', 'append' with 'fail' as default
        '''

        engine = self.init_db_engine()
        dataframe.to_sql(name=table_name, con=engine, if_exists=if_exists, index=False)