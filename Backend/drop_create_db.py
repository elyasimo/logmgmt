import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection parameters
db_params = {
    'dbname': 'postgres',
    'user': 'loguser',
    'password': 'logpassword',
    'host': 'db'
}

def drop_create_database():
    try:
        # Connect to the default 'postgres' database
        conn = psycopg2.connect(**db_params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        # Drop the database if it exists
        cur.execute("DROP DATABASE IF EXISTS logdb")
        logger.info("Dropped database logdb if it existed")

        # Create the database
        cur.execute("CREATE DATABASE logdb")
        logger.info("Created database logdb")

        # Close the cursor and connection
        cur.close()
        conn.close()

        logger.info("Database recreation completed successfully")

    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    drop_create_database()

