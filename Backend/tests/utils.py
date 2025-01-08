from fastapi.testclient import TestClient
from Backend.main import app

client = TestClient(app)

def get_auth_token():
    response = client.post(
        "/token",
        data={"username": "testuser", "password": "testpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200, f"Failed to get auth token: {response.text}"
    return response.json()["access_token"]

def get_auth_headers():
    token = get_auth_token()
    return {"Authorization": f"Bearer {token}"}

