# Purpose: Use the csv files from the output folder to create tables in the defined postgres database

from sqlalchemy import create_engine, MetaData, URL, types, Engine
from sqlalchemy.exc import ProgrammingError
import pandas as pd
from dotenv import load_dotenv
import os
from io import TextIOWrapper
from custom_data_types import custom_data_types #Define any custom data types needed to be explicitely defined
from timeit import default_timer

# Default data_types 
data_types = {
    'created_at': types.DateTime,
    'updated_at': types.DateTime,
    'expires_at': types.DateTime,
    'user_id': types.BigInteger,
}

def sql_loader(df: pd.DataFrame, table_name: str, postgresql_connection: Engine, dtype: dict = data_types, file: TextIOWrapper = None):
    try:
        df.to_sql(table_name, postgresql_connection, dtype=dtype, if_exists='replace',index=False)
    except ProgrammingError as e:
        print(f"Error encountered, switching to default data type definition for table {table_name}")
        if file is not None:
            file.write(f"\n{e}\n")
            file.write("***************************************\n")
        df.to_sql(table_name, postgresql_connection, if_exists='replace',index=False)

if __name__ == "__main__":
    execution_start = default_timer()

    load_dotenv()

    postgresql_connection_str = URL.create(
        drivername='postgresql+psycopg',
        username=os.environ['PG_DB_USERNAME'],
        password=os.environ['PG_DB_PASSWORD'],
        host=os.environ['PG_DB_HOST'],
        port=os.environ['PG_DB_PORT'],
        database=os.environ['PG_DB_DATABASE'],
    )
    postgresql_connection = create_engine(postgresql_connection_str)

    metadata = MetaData()
    metadata.reflect(bind=postgresql_connection)

    file = open(os.path.join(os.path.abspath(os.path.realpath(__file__).replace(os.path.basename(__file__),"")),'errors.log'), "w")
    file.write("Errors encountered when importing csv tables in Postgres Database\n")

    csv_files = os.listdir("./output")
    for csv_file in csv_files:
        path = os.path.abspath(os.path.join(os.path.realpath(__file__).replace(os.path.basename(__file__),""),'output',csv_file))
        print(f"Reading CSV File at {path}")
        df = pd.read_csv(path)
        # if 'id' in df.columns:
        #     df.set_index('id', inplace=True)
        table_name = csv_file.split(".")[0]

        if table_name in custom_data_types.keys():
            sql_loader(df, table_name, postgresql_connection, dtype=custom_data_types[table_name],file=file)
        else:
            sql_loader(df,table_name,postgresql_connection,file=file)

        print(f"Created table {table_name} in postgres database {os.environ['PG_DB_DATABASE']}")

    file.close()
    print(f"Successfully imported csv files into {os.environ['PG_DB_DATABASE']} database")
    print("Table Import Execution time: ",default_timer()-execution_start)
