import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import logging
from sqlalchemy.exc import SQLAlchemyError
import traceback
from sqlalchemy.pool import NullPool

from Backend.main import app
from Backend.api.database import Base, get_db
from Backend.api.models import LogEntry, Customer, Vendor, Device
from Backend.api.config import DATABASE_URL

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Setup test database
engine = create_engine(DATABASE_URL, poolclass=NullPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

def clear_database(db_session):
    try:
        db_session.execute("DELETE FROM logs")
        db_session.execute("DELETE FROM devices")
        db_session.execute("DELETE FROM vendors")
        db_session.execute("DELETE FROM customers")
        db_session.commit()
        logger.debug("Database cleared successfully")
    except SQLAlchemyError as e:
        logger.error(f"Error clearing database: {e}")
        db_session.rollback()
        raise

@pytest.fixture(scope="function")
def sample_logs(db_session):
    logger.debug("Starting sample_logs fixture")
    clear_database(db_session)
    
    now = datetime.utcnow()
    logs = [
        LogEntry(timestamp=now - timedelta(days=1), message="Test log 1", severity="low", vendor="vendor1"),
        LogEntry(timestamp=now - timedelta(hours=12), message="Test log 2", severity="medium", vendor="vendor2"),
        LogEntry(timestamp=now - timedelta(hours=6), message="Test log 3", severity="high", vendor="vendor1"),
        LogEntry(timestamp=now - timedelta(hours=1), message="Test log 4", severity="critical", vendor="vendor3"),
    ]
    db_session.add_all(logs)
    db_session.commit()

    inserted_logs = db_session.query(LogEntry).all()
    assert len(inserted_logs) == 4, f"Expected 4 logs, but found {len(inserted_logs)}"
    for log in inserted_logs:
        logger.debug(f"Log: id={log.id}, timestamp={log.timestamp}, severity={log.severity}, vendor={log.vendor}")

    logger.debug("Finished sample_logs fixture")
    return logs

def test_get_log_counts_by_vendor(db_session, sample_logs):
    logger.debug("Starting test_get_log_counts_by_vendor")
    try:
        logger.debug("Before making request to /api/v1/logs/vendor-counts")
        response = client.get("/api/v1/logs/vendor-counts")
        logger.debug(f"After making request. Response status code: {response.status_code}")
        logger.debug(f"Response content: {response.content}")
        
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
        data = response.json()
        logger.debug(f"Vendor counts response: {data}")
        
        assert len(data) == 3, f"Expected 3 vendors, but found {len(data)}"
        assert data.get("vendor1") == 2, f"Expected 2 logs for vendor1, but found {data.get('vendor1', 0)}"
        assert data.get("vendor2") == 1, f"Expected 1 log for vendor2, but found {data.get('vendor2', 0)}"
        assert data.get("vendor3") == 1, f"Expected 1 log for vendor3, but found {data.get('vendor3', 0)}"
        
        logger.debug("test_get_log_counts_by_vendor completed successfully")
    except Exception as e:
        logger.error(f"Error in test_get_log_counts_by_vendor: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise

def test_get_severity_distribution(db_session, sample_logs):
    logger.debug("Starting test_get_severity_distribution")
    response = client.get("/api/v1/logs/severity-distribution")
    assert response.status_code == 200
    data = response.json()
    logger.debug(f"Severity distribution response: {data}")
    assert len(data) == 4, f"Expected 4 severity levels, but found {len(data)}"
    assert data["low"] == 1, f"Expected 1 low severity log, but found {data.get('low', 0)}"
    assert data["medium"] == 1, f"Expected 1 medium severity log, but found {data.get('medium', 0)}"
    assert data["high"] == 1, f"Expected 1 high severity log, but found {data.get('high', 0)}"
    assert data["critical"] == 1, f"Expected 1 critical severity log, but found {data.get('critical', 0)}"

def test_get_log_count_time_series(db_session, sample_logs):
    logger.debug("Starting test_get_log_count_time_series")
    start_date = (datetime.now() - timedelta(days=2)).isoformat()
    end_date = datetime.now().isoformat()
    response = client.get(f"/api/v1/logs/time-series?start_date={start_date}&end_date={end_date}&interval=day")
    assert response.status_code == 200
    data = response.json()
    logger.debug(f"Time series response: {data}")
    assert len(data) == 2, f"Expected data for 2 days, but found {len(data)}"

def test_get_log_count_time_series_invalid_interval(db_session):
    logger.debug("Starting test_get_log_count_time_series_invalid_interval")
    start_date = (datetime.now() - timedelta(days=2)).isoformat()
    end_date = datetime.now().isoformat()
    response = client.get(f"/api/v1/logs/time-series?start_date={start_date}&end_date={end_date}&interval=invalid")
    assert response.status_code == 400
    assert "Invalid interval" in response.json()["detail"]

def test_get_log_counts_by_vendor_with_date_range(db_session, sample_logs):
    logger.debug("Starting test_get_log_counts_by_vendor_with_date_range")
    start_date = (datetime.now() - timedelta(hours=13)).isoformat()
    end_date = (datetime.now() - timedelta(minutes=30)).isoformat()
    response = client.get(f"/api/v1/logs/vendor-counts?start_date={start_date}&end_date={end_date}")
    assert response.status_code == 200
    data = response.json()
    logger.debug(f"Vendor counts with date range response: {data}")
    assert len(data) == 2, f"Expected 2 vendors, but found {len(data)}"
    assert data["vendor1"] == 1, f"Expected 1 log for vendor1, but found {data.get('vendor1', 0)}"
    assert data["vendor2"] == 1, f"Expected 1 log for vendor2, but found {data.get('vendor2', 0)}"

def test_get_severity_distribution_with_date_range(db_session, sample_logs):
    logger.debug("Starting test_get_severity_distribution_with_date_range")
    start_date = (datetime.now() - timedelta(hours=13)).isoformat()
    end_date = (datetime.now() - timedelta(minutes=30)).isoformat()
    response = client.get(f"/api/v1/logs/severity-distribution?start_date={start_date}&end_date={end_date}")
    assert response.status_code == 200
    data = response.json()
    logger.debug(f"Severity distribution with date range response: {data}")
    assert len(data) == 2, f"Expected 2 severity levels, but found {len(data)}"
    assert data["medium"] == 1, f"Expected 1 medium severity log, but found {data.get('medium', 0)}"
    assert data["high"] == 1, f"Expected 1 high severity log, but found {data.get('high', 0)}"

