import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def recreate_database():
    # Database connection parameters
    params = {
        "host": os.getenv("POSTGRES_HOST", "db"),
        "user": os.getenv("POSTGRES_USER", "loguser"),
        "password": os.getenv("POSTGRES_PASSWORD", "logpassword"),
        "dbname": "postgres"  # Connect to default postgres database
    }

    try:
        # Connect to the default postgres database
        conn = psycopg2.connect(**params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        # Get the name of the database we want to recreate
        db_name = os.getenv("POSTGRES_DB", "logdb")

        # Drop the database if it exists
        cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
        logger.info(f"Dropped database {db_name} if it existed")

        # Create the database
        cur.execute(f"CREATE DATABASE {db_name}")
        logger.info(f"Created database {db_name}")

        # Close the cursor and connection
        cur.close()
        conn.close()

        logger.info("Database recreation completed successfully")
    except Exception as e:
        logger.error(f"An error occurred while recreating the database: {str(e)}")
        raise

if __name__ == "__main__":
    recreate_database()

