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

        ## User Profile Settings Fix
        # Alter Enums to use the empty string value
        enum_cols = ['shown_sat_score_for_me', 'shown_friends_post_for_me', 'show_my_sat_score_to_others', 'show_my_post_to_others']

        for enum_col in enum_cols:
            query = text(f"ALTER TYPE {os.environ['PG_DB_DATABASE']}.public.user_profile_settings_{enum_col}_enum ADD value ''")
            conn.execute(query)
            conn.commit()

            with create_engine(URL.create(drivername='mysql+pymysql', username=os.environ['MYSQL_DB_USERNAME'], password=os.environ['MYSQL_DB_PASSWORD'], 
                                  host=os.environ['MYSQL_DB_HOST'], port=os.environ['MYSQL_DB_PORT'], database=os.environ['MYSQL_DB_DATABASE'])).connect() as con:
                query = text(f"SELECT id from user_profile_settings WHERE {enum_col}=''")
                results = con.execute(query)

            for result in results.fetchall():
                query = text(f"UPDATE {os.environ['PG_DB_DATABASE']}.public.user_profile_settings SET {enum_col}='' WHERE id={result[0]}")
                conn.execute(query)
                conn.commit()

        ## Redirect_to_trustpilot Fix
        query = text(f"ALTER TABLE {os.environ['PG_DB_DATABASE']}.public.ratings ALTER COLUMN redirect_to_trustpilot SET DEFAULT True")
        conn.execute(query)
        conn.commit()        

    print("\nAdditional Fixes implemented")
    print("Execution Time: ",default_timer() - start)