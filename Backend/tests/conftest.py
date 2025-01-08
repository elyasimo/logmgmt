import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Backend.api.database import Base
from Backend.main import app
from fastapi.testclient import TestClient

# Database connection
DATABASE_URL = "postgresql://loguser:logpassword@db:5432/logdb"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def test_app():
    Base.metadata.create_all(bind=engine)
    yield app
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="session")
def test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="session")
def client(test_app):
    return TestClient(test_app)

@pytest.fixture(scope="session")
def auth_headers(client):
    response = client.post(
        "/token",
        data={"username": "testuser", "password": "testpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

