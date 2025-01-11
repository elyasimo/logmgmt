#!/bin/bash

# Wait for the database to be ready
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database is ready!"

# Drop and recreate the database
echo "Dropping and recreating the database..."
python /app/Backend/drop_create_db.py

# Initialize the database
echo "Initializing database..."
python /app/Backend/init_db.py

# Populate the database
echo "Populating database..."
python /app/Backend/populate_db.py

# Start the application
echo "Starting the application..."
cd /app && uvicorn Backend.main:app --host 0.0.0.0 --port 8000 --reload &

# Start sending test logs
echo "Starting test log sender..."
python /app/Backend/generate_logs.py

echo "Starting sample log generation..."
python /app/Backend/scripts/generate_sample_logs.py
