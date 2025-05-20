import pandas as pd
import numpy as np
from datetime import datetime
import re

class DataCleaning:

    def clean_user_data(self, df) -> pd.DataFrame:
        '''
        Cleans user data by:
        - Replacing "NULL" string values with NaN.
        - Removing rows with any Null (NaN) values.
        - Converting the 'join_date' and 'date_of_birth' columns to datetime format.
        - Dropping redundant columns.

        Returns:
            pd.DataFrame: cleaned user data
        '''
        df.replace("NULL", np.nan, inplace=True)
        df.dropna(inplace=True)

        date_cols = ['join_date', 'date_of_birth']

        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                df.dropna(subset=[col], inplace=True)

        redundant_cols = ['level_0', 'Unnamed: 0']
        df = df.drop(columns=[col for col in redundant_cols if col in df.columns])

        return df

    def clean_card_data(self, df) -> pd.DataFrame:
        '''
        Cleans card data by:
        - Replacing "NULL" string values with NaN.
        - Removing rows with any NULL (NaN) values.
        - Removing duplicate card numbers.
        - Removing non-numerical card numbers.
        - Converting 'date_payment_confirmed' and 'expiry_date' column into datetime data type.
        - Dropping redundant columns.
        
        Returns:
            pd.DataFrame: cleaned card data
        '''
        df.replace("NULL", np.nan, inplace=True)
        df.dropna(inplace=True)
        df.drop_duplicates(subset=['card_number'], inplace=True)
        df = df[df['card_number'].astype(str).str.isdigit()]
        df['card_number_id'] = df['card_number'].astype(str).str[0:10]  # Deals with problem where many entries in orders table have replaced final digits with 0's

        date_cols = ['date_payment_confirmed', 'expiry_date']

        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                df.dropna(subset=[col], inplace=True)

        redundant_cols = ['level_0', 'Unnamed: 0']
        df = df.drop(columns=[col for col in redundant_cols if col in df.columns])

        return df
    
    def clean_store_data(self, df) -> pd.DataFrame:
        '''
        Cleans store data by:
        - Replacing "NULL" string values with NaN.
        - Removing rows with any NULL (NaN) values.
        - Coverting "opening_date" column into datetime data type.
        - Dropping redundant columns.
        - Stripping away symbols, letters and white spaces from "staff_number" column.
        
        Returns:
            pd.DataFrame: cleaned store data
        '''
        redundant_cols = ['level_0', 'Unnamed: 0', 'lat']
        df = df.drop(columns=[col for col in redundant_cols if col in df.columns])
        
        date_formats = ["%Y-%m-%d", "%b %Y %d", "%Y %b %d"]

        def parse_dates(date_str, date_formats):
            for format in date_formats:
                try:
                    return pd.to_datetime(date_str, format=format)
                except ValueError:
                    pass
            return pd.NaT

        df['opening_date'] = df['opening_date'].apply(lambda x: parse_dates(x, date_formats))
        df.dropna(subset=['opening_date'], inplace=True)

        df['staff_numbers'] = df['staff_numbers'].str.replace(r'[^0-9]', '', regex=True)
        df['staff_numbers'] = pd.to_numeric(df['staff_numbers'], errors='coerce')
        df.dropna(subset=['staff_numbers'], inplace=True)

        df.replace("NULL", np.nan, inplace=True)
        df.dropna(inplace=True)

        return df

    def convert_product_weights(self, df: pd.DataFrame) -> pd.DataFrame:
        '''
        Cleans and converts all values in 'weight' column to kg.

        Returns:
            pd.DataFrame: data with cleaned and converted 'weights' column.
        '''
        df.dropna(inplace=True)

        def extract_weight_and_unit(weight_str: str):
            match = re.match(r'(\d+\.?\d*)(kg|g|ml|oz)', weight_str)
            if match:
                val = float(match.group(1))
                unit = match.group(2)
                return val, unit
            return None, None

        def convert_to_kg(val, unit):
            if unit == 'kg':
                return val
            elif unit == 'g':
                return val * 0.001
            elif unit == 'ml':
                return val * 0.001
            elif unit =='oz':
                return val * 0.0283495

        df['weight'] = df['weight'].apply(lambda x: convert_to_kg(*extract_weight_and_unit(x)))

        return df



    def clean_products_data(self, df: pd.DataFrame) -> pd.DataFrame:
        '''
        Cleans product data by:
        - Replacing string "NULL" values with NaN
        - Removing rows with NaN values
        - Removing redundant columns
        - Converting "date_added" column into datetime format
        - Cleaning and converting all values in 'weight' column to kg

        Returns:
            pd.DataFrame: cleaned products data
        '''
        df.replace("NULL", np.nan, inplace=True)
        df.dropna(inplace=True)
        
        redundant_cols = ['level_0', 'Unnamed: 0']
        df = df.drop(columns=[col for col in redundant_cols if col in df.columns])

        date_cols = ['date_added']

        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                df.dropna(subset=[col], inplace=True)

        df = self.convert_product_weights(df)

        return df

    def clean_orders_data(self, df: pd.DataFrame) -> pd.DataFrame:
        '''
        Cleans orders data by:
        - Removing redundant columns

        Returns:
            pd.DataFrame: cleaned orders data
        '''
        redundant_cols = ['level_0', 'Unnamed: 0', 'first_name', 'last_name', '1']
        df = df.drop(columns=[col for col in redundant_cols if col in df.columns])

        df.drop_duplicates(subset=['card_number'], inplace=True)
        df = df[df['card_number'].astype(str).str.isdigit()]
        df['card_number_id'] = df['card_number'].astype(str).str[0:10] # Deals with problem where many entries in orders table have replaced final digits with 0's

        return df

    def clean_dates_details(self, df: pd.DataFrame) -> pd.DataFrame:
        '''
        Cleans dates data by:
        - Replacing "NULL" strings with NaN
        - Removing NaN values
        - Converting 'day', 'month' and 'year' columns into numeric values or NaN
        
        Returns:
            pd.DataFrame: cleaned dates data
        '''
        df.replace("NULL", np.nan, inplace=True)
        df.dropna(inplace=True)
        
        numeric_cols = ['day', 'month', 'year']
        
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')

        return df
