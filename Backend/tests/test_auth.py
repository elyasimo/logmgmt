import pytest
from fastapi.testclient import TestClient
from Backend.main import app

client = TestClient(app)

def test_login():
    user_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = client.post("/api/v1/login", data=user_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_logout():
    response = client.post("/api/v1/logout")
    assert response.status_code == 200

