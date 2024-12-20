#!/usr/bin/python3

# Purpose: To extract MySQL Database tables into CSV Files

from sqlalchemy import create_engine, MetaData, URL 
import pandas as pd
from dotenv import load_dotenv
import os
from os import environ
from timeit import default_timer

if __name__ == "__main__":
    execution_start = default_timer()

    # Setting up output folder in same directory
    try:
        output_folder_path = os.path.join(
                                    os.path.abspath(os.path.realpath(__file__).replace(os.path.basename(__file__),"")),
                                    "output")
        os.mkdir(output_folder_path)
        print(f"Set up new output directory at {output_folder_path}")
    except OSError as e:
        print(e)

    print("Extracting variables from .env")
    load_dotenv()

    print(f"Connecting to Defined Database: {environ['MYSQL_DB_DATABASE']}")
    mysql_connection_str = URL.create(
        drivername='mysql+pymysql',
        username=environ['MYSQL_DB_USERNAME'],
        password=environ['MYSQL_DB_PASSWORD'],
        host=environ['MYSQL_DB_HOST'],
        port=environ['MYSQL_DB_PORT'],
        database=environ['MYSQL_DB_DATABASE'],
    )
    mysql_connection = create_engine(mysql_connection_str)

    metadata = MetaData()
    metadata.reflect(bind=mysql_connection)

    print(f"Extracting tables from database {environ['MYSQL_DB_DATABASE']}")
    table_names = metadata.tables.keys()
    for table_name in table_names:
        query = f"SELECT * from {table_name}"
        df = pd.read_sql(query, mysql_connection)
        output_path = f'output/{table_name}.csv'
        print(f"Writing csv output to file at {output_path} for table {table_name}")
        df.to_csv(output_path, index=False)
        print(f"Successfully extracted csv output for table {table_name}")

    print(f"Successfully exported tables to csv files from Database {environ['MYSQL_DB_DATABASE']}. Check out the output folder")
    print("Table Export Execution Time: ",default_timer()-execution_start)