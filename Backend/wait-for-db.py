import time
import psycopg2
import os

def wait_for_db():
    db_params = {
        "dbname": os.getenv("POSTGRES_DB", "logdb"),
        "user": os.getenv("POSTGRES_USER", "loguser"),
        "password": os.getenv("POSTGRES_PASSWORD", "logpassword"),
        "host": os.getenv("POSTGRES_HOST", "db"),
        "port": os.getenv("POSTGRES_PORT", "5432"),
    }

    max_retries = 30
    retry_interval = 2

    for _ in range(max_retries):
        try:
            conn = psycopg2.connect(**db_params)
            conn.close()
            print("Database is ready!")
            return
        except psycopg2.OperationalError:
            print("Waiting for database...")
            time.sleep(retry_interval)

    print("Failed to connect to the database after multiple attempts.")
    exit(1)

if __name__ == "__main__":
    wait_for_db()

