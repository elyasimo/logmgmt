FROM python:3.9-slim-buster

# Set environment variables
ARG SETUPTOOLS_USE_DISTUTILS=stdlib
ENV SETUPTOOLS_USE_DISTUTILS=$SETUPTOOLS_USE_DISTUTILS

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libldap2-dev \
    libsasl2-dev \
    libssl-dev \
    python3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*
    
WORKDIR /app

# Copy the entire Backend directory
COPY Backend /app/Backend

# Copy requirements file
COPY Backend/requirements.txt /app/

# Install psycopg2 dependencies and netcat-openbsd
RUN apt-get update && apt-get install -y libpq-dev netcat-openbsd

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Install Alembic with timezone support
RUN pip install alembic[tz] python-dateutil

# Set the Python path
ENV PYTHONPATH=/app

# Make sure the scripts are executable and have Unix line endings
RUN chmod +x /app/Backend/start.sh && \
    chmod +x /app/Backend/scripts/generate_sample_logs.py && \
    sed -i 's/\r$//' /app/Backend/start.sh && \
    sed -i 's/\r$//' /app/Backend/scripts/generate_sample_logs.py

# Use the start.sh script as the entry point
CMD ["/bin/bash", "/app/Backend/start.sh"]

