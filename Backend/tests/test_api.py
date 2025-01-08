import pytest
from fastapi.testclient import TestClient
from Backend.main import app
from datetime import datetime, timedelta
from .utils import get_auth_headers

client = TestClient(app)

def test_get_logs():
    headers = get_auth_headers()
    response = client.get("/api/v1/logs", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_logs_with_filters():
    headers = get_auth_headers()
    response = client.get("/api/v1/logs?level=INFO&source=test_source&limit=10", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) <= 10

def test_get_log_stats():
    headers = get_auth_headers()
    response = client.get("/api/v1/logs/stats", headers=headers)
    assert response.status_code == 200
    assert "total_logs" in response.json()
    assert "level_counts" in response.json()
    assert "source_counts" in response.json()

def test_search_logs():
    headers = get_auth_headers()
    response = client.get("/api/v1/logs/search?query=test", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_ingest_log():
    headers = get_auth_headers()
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "level": "INFO",
        "source": "test_source",
        "message": "Test log message"
    }
    response = client.post("/api/v1/ingest", json=log_entry, headers=headers)
    assert response.status_code == 200

def test_end_to_end():
    headers = get_auth_headers()
    # Ingest a log
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "level": "ERROR",
        "source": "test_source",
        "message": "Test error message"
    }
    ingest_response = client.post("/api/v1/ingest", json=log_entry, headers=headers)
    assert ingest_response.status_code == 200

    # Search for the log
    search_response = client.get("/api/v1/logs/search?query=error", headers=headers)
    assert search_response.status_code == 200
    assert len(search_response.json()) > 0

    # Get log stats
    stats_response = client.get("/api/v1/logs/stats", headers=headers)
    assert stats_response.status_code == 200
    assert stats_response.json()["level_counts"].get("ERROR", 0) > 0

