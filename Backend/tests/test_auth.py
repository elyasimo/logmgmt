import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Backend.main import app
from Backend.api.database import Base, get_db
from Backend.api.models import User
from Backend.api.dependencies import get_password_hash

# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    # Setup: create test user
    db = TestingSessionLocal()
    hashed_password = get_password_hash("testpassword")
    test_user = User(username="testuser", email="test@example.com", hashed_password=hashed_password)
    db.add(test_user)
    db.commit()
    
    yield
    
    # Teardown: clear database
    db.query(User).delete()
    db.commit()

def test_register():
    response = client.post(
        "/api/v1/register",
        json={"username": "newuser", "email": "newuser@example.com", "password": "StrongPass1!"}
    )
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["username"] == "newuser"

def test_login():
    response = client.post(
        "/api/v1/login",
        data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

def test_refresh_token():
    # First, login to get the refresh token
    login_response = client.post(
        "/api/v1/login",
        data={"username": "testuser", "password": "testpassword"}
    )
    refresh_token = login_response.json()["refresh_token"]

    # Now use the refresh token to get a new access token
    refresh_response = client.post(
        "/api/v1/refresh",
        json={"refresh_token": refresh_token}
    )
    assert refresh_response.status_code == 200
    assert "access_token" in refresh_response.json()

def test_logout():
    # First, login to get the access token
    login_response = client.post(
        "/api/v1/login",
        data={"username": "testuser", "password": "testpassword"}
    )
    access_token = login_response.json()["access_token"]

    # Now logout
    logout_response = client.post(
        "/api/v1/logout",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert logout_response.status_code == 200
    assert logout_response.json()["message"] == "Successfully logged out"

def test_protected_route():
    # First, login to get the access token
    login_response = client.post(
        "/api/v1/login",
        data={"username": "testuser", "password": "testpassword"}
    )
    access_token = login_response.json()["access_token"]

    # Test accessing a protected route (assuming /api/v1/protected exists)
    protected_response = client.get(
        "/api/v1/protected",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert protected_response.status_code == 200

    # Test accessing with invalid token
    invalid_response = client.get(
        "/api/v1/protected",
        headers={"Authorization": "Bearer invalidtoken"}
    )
    assert invalid_response.status_code == 401

