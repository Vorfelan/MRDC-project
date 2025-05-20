import yaml
from sqlalchemy import create_engine, inspect, text, MetaData
from sqlalchemy.engine.base import Engine
import pandas as pd
from pathlib import Path


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
        Returns a list of all tables in database.
        '''

        engine = self.init_db_engine()
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        return tables


    def list_cols_in_table(self, table_name):
        '''
        Prints a list of columns and corresponding data types for specified table.

        Args:
            table_name (str): Name of table within database for which columns are to be listed.
        '''

        engine = self.init_db_engine()
        inspector = inspect(engine)
        columns = inspector.get_columns(table_name)

        for col in columns:
            print(f"{col['name']}: {col['type']}")


    def get_table_from_db(self, table_name):
        '''
        Returns specified table from SQL database as pd.DataFrame
        '''

        engine = self.init_db_engine()
        return pd.read_sql_table(table_name, con=engine)


    def upload_to_db(self, dataframe: pd.DataFrame, table_name: str, if_exists: str = 'replace'):
        '''
        Uploads a DataFrame to a table in the database.
        
        Args:
            dataframe (pd.DataFrame): the DataFrame to upload
            table_name (str): name of table to upload to
            if_exists (str): what to do if table already exists. Options are 'fail', 'replace', 'append' with 'fail' as default
        '''

        engine = self.init_db_engine()
        dataframe.to_sql(name=table_name, con=engine, if_exists=if_exists, index=False)


    def execute_sql_list(self, sql_commands):
        '''
        Executes a list of SQL command strings on connected database.
        
        Args:
            sql_commands (list of str): A list of SQL commands to execute.
        '''

        engine = self.init_db_engine()
        with engine.connect() as conn:
            for sql in sql_commands:
                conn.execute(text(sql))
        
        print("All SQL commands executed.")


    def execute_sql_from_folder(self, folder_name):
        '''
        Executes a list of SQL commands found in individual files within a specified folder.

        Args:
            folder_name (str): folder containing files with SQL commands to be executed.
        '''

        sql_dir = Path(folder_name)
        sql_files = sql_dir.glob("*.sql")

        queries = []
        for file in sql_files:
            sql_commands = file.read_text(encoding='utf-8').strip()
            for command in sql_commands.split(";"):
                if command.strip():
                    queries.append(command)

        self.execute_sql_list(queries)


    def return_query(self, query):
        '''
        Executes SQL query and returns result as a pd.DataFrame.

        Args:
            query (str): SQL query to execute.

        Returns:
            pd.DataFrame: Result of query.
        '''

        engine = self.init_db_engine()
        with engine.connect() as conn:
            result = conn.execute(text(query))
            rows = result.fetchall()
            keys = result.keys()
            data = [dict(zip(keys, row)) for row in rows]

        return pd.DataFrame(data)


    def return_query_from_file(self, file_name):
        '''
        Executes SQL query from specified file and returns result as a pd.DataFrame.
        
        Args:
            file_name (str): Name of file containing SQL query to execute (.sql extention already added).

        Returns:
            pd.DataFrame: Result of query.
        '''
        
        file_path = Path(f'SQL_queries/{file_name}.sql')
        query = file_path.read_text(encoding='utf-8').strip()
        return self.return_query(query)
    
    
    def clear_database(self):
        '''
        CAREFUL - this will remove all tables from your database.
        '''
        engine = self.init_db_engine()
        meta = MetaData()
        meta.reflect(bind=engine)
        meta.drop_all(bind=engine)
        print("All tables have been removed from SQL database.")

