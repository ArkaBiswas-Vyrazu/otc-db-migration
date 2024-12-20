# Purpose: To export the view from OTC MySQL Database to OTC Postgresql Database
# Specific only to migrating OTC Database

from sqlalchemy import create_engine, URL, text
import pandas as pd
from dotenv import load_dotenv
import os
from timeit import default_timer

if __name__ == "__main__":
    start = default_timer()

    # Reading SQL from file
    sql_file = open("./view_sql.sql","r")
    query = sql_file.read()
    sql_file.close()

    load_dotenv()

    postgresql_connector_str = URL.create(
        drivername='postgresql+psycopg',
        username=os.environ['PG_DB_USERNAME'],
        password=os.environ['PG_DB_PASSWORD'],
        host=os.environ['PG_DB_HOST'],
        port=os.environ['PG_DB_PORT'],
        database=os.environ['PG_DB_DATABASE']
    )
    postgresql_connector = create_engine(postgresql_connector_str)    
    
    with postgresql_connector.connect() as conn:
        conn.execute(text(query))
        conn.commit()
        print(f"\nView feed_data added to {os.environ['PG_DB_DATABASE']} database")
        print("Execution Time: ",default_timer() - start)