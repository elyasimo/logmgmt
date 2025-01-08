import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from Backend.main import app
from Backend.api.routes.logs import logs_db
from Backend.api.models import LogEntry
from .utils import get_auth_headers

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_logs_db():
    logs_db.clear()
    yield
    logs_db.clear()

def test_create_log():
    headers = get_auth_headers()
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "level": "INFO",
        "source": "test_source",
        "message": "Test log message"
    }
    response = client.post("/api/v1/logs", json=log_entry, headers=headers)
    assert response.status_code == 200
    assert response.json() == log_entry

def test_get_logs_pagination():
    headers = get_auth_headers()
    # Create 150 log entries
    for i in range(150):
        log_entry = LogEntry(
            timestamp=datetime.now() + timedelta(minutes=i),
            level="INFO",
            source="test_source",
            message=f"Test log message {i}"
        )
        logs_db.append(log_entry)

    # Test first page
    response = client.get("/api/v1/logs?page=1&page_size=100", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 100

    # Test second page
    response = client.get("/api/v1/logs?page=2&page_size=100", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 50

def test_get_logs_filtering():
    headers = get_auth_headers()
    # Create log entries with different levels and sources
    levels = ["INFO", "WARNING", "ERROR"]
    sources = ["source1", "source2"]
    base_time = datetime.now()
    for i in range(60):
        log_entry = LogEntry(
            timestamp=base_time + timedelta(minutes=i),
            level=levels[i % 3],
            source=sources[i % 2],
            message=f"Test log message {i}"
        )
        logs_db.append(log_entry)

    # Test filtering by level
    response = client.get("/api/v1/logs?level=INFO", headers=headers)
    assert response.status_code == 200
    assert all(log["level"] == "INFO" for log in response.json())

    # Test filtering by source
    response = client.get("/api/v1/logs?source=source1", headers=headers)
    assert response.status_code == 200
    assert all(log["source"] == "source1" for log in response.json())

    # Test filtering by time range
    start_time = base_time.isoformat()
    end_time = (base_time + timedelta(minutes=30)).isoformat()
    response = client.get(f"/api/v1/logs?start_time={start_time}&end_time={end_time}", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 31  # 31 minutes (inclusive end)

def test_search_logs():
    headers = get_auth_headers()
    # Create log entries with different messages
    for i in range(50):
        log_entry = LogEntry(
            timestamp=datetime.now() + timedelta(minutes=i),
            level="INFO",
            source="test_source",
            message=f"Test log message {i}"
        )
        logs_db.append(log_entry)

    # Test search functionality
    response = client.get("/api/v1/logs/search?query=message 25", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["message"] == "Test log message 25"

def test_get_log_stats():
    headers = get_auth_headers()
    # Create log entries with different levels and sources
    levels = ["INFO", "WARNING", "ERROR"]
    sources = ["source1", "source2"]
    for i in range(60):
        log_entry = LogEntry(
            timestamp=datetime.now() + timedelta(minutes=i),
            level=levels[i % 3],
            source=sources[i % 2],
            message=f"Test log message {i}"
        )
        logs_db.append(log_entry)

    response = client.get("/api/v1/logs/stats", headers=headers)
    assert response.status_code == 200
    stats = response.json()
    assert stats["total_logs"] == 60
    assert stats["level_counts"] == {"INFO": 20, "WARNING": 20, "ERROR": 20}
    assert stats["source_counts"] == {"source1": 30, "source2": 30}

