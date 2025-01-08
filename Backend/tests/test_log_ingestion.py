import pytest
import asyncio
import httpx
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from Backend.api.models import DBLogEntry, Base
from Backend.api.database import get_db
from Backend.main import app
from fastapi.testclient import TestClient
import logging
import time

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Database connection
DATABASE_URL = "postgresql://loguser:logpassword@db:5432/logdb"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# API URL
API_URL = "http://api:8000"

@pytest.fixture(scope="module")
def test_app():
    logger.debug("Setting up test_app fixture")
    Base.metadata.create_all(bind=engine)
    yield app
    Base.metadata.drop_all(bind=engine)
    logger.debug("Tearing down test_app fixture")

@pytest.fixture(scope="module")
def test_db():
    logger.debug("Setting up test_db fixture")
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        logger.debug("Tearing down test_db fixture")

@pytest.fixture(scope="module")
def client(test_app):
    logger.debug("Setting up client fixture")
    with TestClient(test_app) as client:
        yield client
    logger.debug("Tearing down client fixture")

@pytest.fixture(scope="module")
def auth_headers(client):
    logger.debug("Getting auth headers")
    response = client.post(
        "/token",
        data={"username": "testuser", "password": "testpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_ingest_log(client, auth_headers, test_db):
    logger.debug("Starting test_ingest_log")
    start_time = time.time()
    log_entries = [
        {
            "timestamp": datetime.utcnow().isoformat(),
            "level": "INFO",
            "source": "test_script",
            "message": f"Test log message {i}"
        } for i in range(150)  # Create 150 log entries
    ]

    for i, log_entry in enumerate(log_entries):
        logger.debug(f"Ingesting log entry {i+1}")
        response = client.post("/api/v1/ingest", json=log_entry, headers=auth_headers)
        assert response.status_code == 200
        result = response.json()
        assert "message" in result
        assert "log_id" in result
        if (i+1) % 10 == 0:
            logger.debug(f"Ingested {i+1} logs")

    logger.debug("Querying ingested logs")
    logs = test_db.query(DBLogEntry).all()
    assert len(logs) >= 150
    for log in logs[:5]:  # Print first 5 logs for verification
        logger.debug(f"Log ID: {log.id}, Timestamp: {log.timestamp}, Level: {log.level}, Source: {log.source}, Message: {log.message}")
    logger.debug(f"Finished test_ingest_log in {time.time() - start_time:.2f} seconds")

def test_get_logs_pagination(client, auth_headers):
    logger.debug("Starting test_get_logs_pagination")
    start_time = time.time()
    
    logger.debug("Testing first page")
    response = client.get("/api/v1/logs?page=1&page_size=50", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 50
    assert data["page"] == 1
    assert data["page_size"] == 50
    assert data["total"] >= 150
    assert data["total_pages"] >= 3

    logger.debug("Testing second page")
    response = client.get("/api/v1/logs?page=2&page_size=50", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 50
    assert data["page"] == 2

    logger.debug("Testing last page")
    last_page = data["total_pages"]
    response = client.get(f"/api/v1/logs?page={last_page}&page_size=50", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) <= 50
    assert data["page"] == last_page
    logger.debug(f"Finished test_get_logs_pagination in {time.time() - start_time:.2f} seconds")

def test_search_logs_pagination(client, auth_headers):
    logger.debug("Starting test_search_logs_pagination")
    start_time = time.time()
    
    logger.debug("Testing search with pagination")
    response = client.get("/api/v1/logs/search?query=Test&page=1&page_size=50", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) <= 50
    assert data["page"] == 1
    assert data["page_size"] == 50
    assert "total" in data
    assert "total_pages" in data

    if data["total_pages"] > 1:
        logger.debug("Testing second page of search results")
        response = client.get("/api/v1/logs/search?query=Test&page=2&page_size=50", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) <= 50
        assert data["page"] == 2
    logger.debug(f"Finished test_search_logs_pagination in {time.time() - start_time:.2f} seconds")

def test_advanced_search(client, auth_headers, test_db):
    logger.debug("Starting test_advanced_search")
    start_time = time.time()

    # Insert some test logs
    test_logs = [
        DBLogEntry(timestamp=datetime.utcnow(), level="INFO", source="test_source", message="Test log message 1"),
        DBLogEntry(timestamp=datetime.utcnow(), level="ERROR", source="test_source", message="Error occurred in module XYZ"),
        DBLogEntry(timestamp=datetime.utcnow(), level="WARNING", source="another_source", message="Warning: disk space low"),
    ]
    test_db.add_all(test_logs)
    test_db.commit()

    # Test regex search
    logger.debug("Testing regex search")
    response = client.get("/api/v1/search?search_query=Error.*XYZ&use_regex=true", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["message"] == "Error occurred in module XYZ"

    # Test field-specific search
    logger.debug("Testing field-specific search")
    response = client.get("/api/v1/search?search_query=WARNING&fields=level", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["level"] == "WARNING"

    # Test combined search
    logger.debug("Testing combined search")
    response = client.get("/api/v1/search?search_query=disk&fields=message&fields=source", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["message"] == "Warning: disk space low"
    assert data["items"][0]["source"] == "another_source"

    logger.debug(f"Finished test_advanced_search in {time.time() - start_time:.2f} seconds")

logger.debug("All test functions defined")

