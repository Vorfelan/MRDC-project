# Multinational Retail Data Centralisation project

## Overview

This project pulls together sales data from a mutlinational retail company, from SQL database and AWS S3 bucket sources, and centralises all into a fresh, ordered SQL database. This data includes company store details, customer and card details, product details and records of orders made and corresponding dates and times. Connection to SQL databases via python is facilitated by a DatabaseConnector class which uses SQLAlchemy. Data is extracted from original sources using a DataExtractor class, cleaned using a DataCleaning class, before being input into a new SQL database where a rigid schema is established. Finally, a number of queries are executed on the new database to inspect the geographical spread of stores, staff headcounts and various sales data over various measures of time and location.

## Aims & Experience Gained

This project is an endeavour to familiarise myself with working with SQL databases and toolkits/adapters for managing databases and executing queries using python, including SQLAlchemy. It has given me some experience working with AWS and thorough experience cleaning various threads of data and bringing them together to create a functional relational database schema, and constructing robust queries to effectively utilise the database to answer specific business questions.

## Usage

Please feel free to use this code as a reference for playing with your own databases. The Jupyter notebook files are the place to start with surface outline of the process. 
First, the file 'prepare_cleaned_SQL_database.ipynb' extracts the data from various sources, cleans each data table, uploads to the new SQL database and establishes the database schema. This notebook utilises classes and functions defined within the database_utils.py, data_extraction.py and data_cleaning.py scripts. It also utilises SQL scripts found within the SQL_tidy_commands folder to update and organise the clean database. The excel file 'db_relationships.xlsx' helps to understand the key relational columns shared between the orders_table and other tables.
Second, the file 'data_queries.ipynb' inspects the clean SQL database, returning the results from specific queries about the company sales and business. Here, SQLAlchemy and the DatabaseConnector class (defined in database_utils.py) are used to read queries which are stored in SQL files in the SQL_queries folder.

## File structure

### Execution files:
- prepare_cleaned_SQL_database.ipynb
- data_queries.ipynb

### Source code:
- database_utils.py
- data_extraction.py
- data_cleaning.py

### Data files:
- date_details.json
- product_data.xlsx

### SQL scripts:
- scripts for organising the clean database within SQL_tidy_commands folder
- scripts for querying the data within SQL_queries folder

### Credential files:
- Credentials for acessing SQL databases are within 'credentials' folder but set to .gitignore.

### Other:
- 'db_relationships.xlsx' contains table of shared columns between tables in clean database, i.e. identifies primary and foreign keys.


## Notes
I think there are still some issues with this code, where more data than necessary might have been removed when forced to solve certain issues, including discrepancies between rows in the orders table foreign keys and corresponding tables. These will have to be addressed later.
