#!/usr/bin/python3

# Purpose: To extract MySQL Database tables into CSV Files

from sqlalchemy import create_engine, MetaData, URL 
from sqlalchemy.types import Time
import pandas as pd
from dotenv import load_dotenv
import os
from os import environ
from timeit import default_timer
from custom_data_types import custom_data_types
import csv

def checkForTimeFields(table_name: str):
    if table_name not in custom_data_types:
        return False

    time_field_exists = False
    for field in custom_data_types[table_name]:
        if custom_data_types[table_name][field] == Time:
            time_field_exists = True

    if not time_field_exists:
        return False
    
    return True

def fixTimeFields(table_name: str):
    file_path = f"./output/{table_name}.csv"
    
    rows = []
    for row in csv.reader(open(file_path)):
        rows.append(row)

    # Very naive approach, but it should work
    # There is probably a better way to do this
    for row in rows:
        for index in range(len(row)):
            if '0 days' in row[index]:
                row[index] = row[index].replace("0 days","").strip()
                if row[index] == '':
                    row[index] = '00:00:00'
    
    writer = csv.writer(open(file_path,'w'))
    writer.writerows(rows)
    
    print(f"Fixed Time Fields in table {table_name}")


def fixTimeStampFields(table_name: str):
    file_path = f"./output/{table_name}.csv"

    rows = []
    for row in csv.reader(open(file_path)):
        rows.append(row)

    detected = False
    for row in rows:
        for index in range(len(row)):
            if '0000-00-00 00:00:00' in row['index']:
                detected = True
                row[index] = ''

    writer = csv.writer(open(file_path, 'w'))
    writer.writerows(rows)

    if detected:
        print(f'Fixed Timestamp Fields in table {table_name}')

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

        # Filtering the time problem (Use the custom_data_types file for this feature) 
        if checkForTimeFields(table_name):
            fixTimeFields(table_name) 

        # Fixing the 0000-00-00 00:00:00 error
        fixTimeStampFields(table_name)

    print(f"Successfully exported tables to csv files from Database {environ['MYSQL_DB_DATABASE']}. Check out the output folder")
    print("Table Export Execution Time: ",default_timer()-execution_start)