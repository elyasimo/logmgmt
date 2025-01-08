FROM python:3.9

WORKDIR /app

# Copy the entire Backend directory
COPY Backend /app/Backend

# Copy requirements file
COPY Backend/requirements.txt /app/

# Install psycopg2 dependencies and netcat-openbsd
RUN apt-get update && apt-get install -y libpq-dev netcat-openbsd

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Install Alembic with timezone support
RUN pip install alembic[tz] python-dateutil

# Set the Python path
ENV PYTHONPATH=/app

# Make sure the start.sh script is executable
RUN chmod +x /app/Backend/start.sh

# Use the start.sh script as the entry point
CMD ["/bin/bash", "/app/Backend/start.sh"]

