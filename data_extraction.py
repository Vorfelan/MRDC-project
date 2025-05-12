import pandas as pd
from sqlalchemy import create_engine, inspect
from sqlalchemy.engine.base import Engine
from database_utils import DatabaseConnector
import boto3
import requests
import os

class DataExtractor:
    def __init__(self, credentials_path: str):
        self.credentials_path = credentials_path
        self.db_connector = DatabaseConnector(credentials_path)

    def read_rds_table(self, table_name: str) -> pd.DataFrame:
        '''
        Reads data from the specified tables in the database and returns as pandas DataFrame.
        
        Args:
            table_name (str): Name of table to query.
            
        Returns:
            pd.FataFrame: A pandas DataFrame containing data from specified table.
        '''
        engine = self.db_connector.init_db_engine()   # Get engine from DatabaseConnector
        query = f"SELECT * FROM {table_name}"   # SQL query to select all data from specified table
        df = pd.read_sql(query, engine)   # Use pandas to execute query & return DataFrame result
        return df
    
    def extract_from_s3(self, url_path: str, new_file_name: str) -> pd.DataFrame:
        '''
        Downloads and saves CSV data from AWS S3 bucket via specified url_path, reads downloaded
        CSV file into pandas DataFrame and returns this.

        Args:
            url_path (str): url path for S3 bucket and file.
            new_file_name (str): name for new file downloaded (without extension).

        Returns:
            pd.DataFrame: A pandas DataFrame containing data downloaded from S3 bucket.
        '''

        file_ext = url_path.split('.')[-1]  # Detects if it's .csv or .json

        url_parts = url_path.replace("s3://", "").split("/", 1)
        bucket_name = url_parts[0]
        file_name = url_parts[1]

        s3 = boto3.client('s3')
        s3.download_file(bucket_name, file_name, f'{new_file_name}.{file_ext}')
        if file_ext == 'csv':
            df = pd.read_csv(f'{new_file_name}.csv')
        if file_ext == 'json':
            df = pd.read_json(f'{new_file_name}.json')
        return df
    
    #def extract_from_http_url(self, url_path: str, new_file_name: str) -> pd.DataFrame:
    #    '''
    #    Downloads data from a public HTTP URL specifed by url_path and returns as DataFrame.
    #    
    #    Args:
    #        url_path (str): public HTTP URL path.
    #        new_file_name (str): name fpr new file downloaded (without extension).
    #        
    #    Returns:
    #        pd.DataFrame: A pandas DataFrame containing downloaded data.
    #    '''
    