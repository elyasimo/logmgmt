import pytest
from fastapi.testclient import TestClient
from Backend.main import app
from Backend.api.models import Alert
from .utils import get_auth_headers

client = TestClient(app)

def test_get_alerts():
    headers = get_auth_headers()
    response = client.get("/api/v1/alerts", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_alert():
    headers = get_auth_headers()
    alert_data = {
        "name": "Test Alert",
        "query": "level:error",
        "severity": "high"
    }
    response = client.post("/api/v1/alerts", json=alert_data, headers=headers)
    assert response.status_code == 201, f"Failed to create alert: {response.text}"
    created_alert = response.json()
    assert created_alert["name"] == alert_data["name"]
    assert created_alert["query"] == alert_data["query"]
    assert created_alert["severity"] == alert_data["severity"]
    assert "id" in created_alert
    assert isinstance(created_alert["id"], int)

def test_create_alert_with_id():
    headers = get_auth_headers()
    alert_data = {
        "id": 100,
        "name": "Test Alert with ID",
        "query": "level:warning",
        "severity": "medium"
    }
    response = client.post("/api/v1/alerts", json=alert_data, headers=headers)
    assert response.status_code == 201, f"Failed to create alert: {response.text}"
    created_alert = response.json()
    assert created_alert == alert_data

