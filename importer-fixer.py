#!/usr/bin/python3

"""
    Purpose: Adding additional fixes to the database
    NOTE: The fixes provided here are exclusive to the OTC Database
"""

from sqlalchemy import create_engine, URL, text
import os
from timeit import default_timer
from dotenv import load_dotenv

if __name__ == "__main__":
    start = default_timer()

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

    with postgresql_connection.connect() as conn:
        # Subject Model Fix
        query = text(f"UPDATE {os.environ['PG_DB_DATABASE']}.public.subject SET video = '' WHERE video IS NULL")
        conn.execute(query)
        conn.commit()

        # User Model Fix
        query = text(f"UPDATE {os.environ['PG_DB_DATABASE']}.public.user SET last_name = '' WHERE last_name IS NULL")
        conn.execute(query)
        conn.commit()

    print("\nAdditional Fixes implemented")
    print("Execution Time: ",default_timer() - start)