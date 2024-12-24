#!/usr/bin/python3

"""Purpose: [EXCLUSIVE TO THE OTC DATABASE] Adding additional fixes to the database"""

from sqlalchemy import create_engine, URL, text
import os
from timeit import default_timer

if __name__ == "__main__":
    start = default_timer()

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
    print("\nExecution Time: ",default_timer() - start)