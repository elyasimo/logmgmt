from Backend.api.dependencies import get_password_hash
from Backend.api.models import User, Customer, Vendor, Device, LogEntry, ChangelogEntry, SeverityEnum
from Backend.api.database import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import json
import random
from datetime import datetime, timedelta

def populate_db():
    db = SessionLocal()
    try:
        # Create a test user
        hashed_password = get_password_hash("testpassword")
        test_user = User(
            username="testuser",
            email="testuser@example.com",
            hashed_password=hashed_password,
            is_active=True,
            role="user"
        )
        db.add(test_user)

        # Create some test customers
        customer1 = Customer(cnnid="CNN001", name="Customer 1")
        customer2 = Customer(cnnid="CNN002", name="Customer 2")
        db.add_all([customer1, customer2])

        # Create some test vendors
        vendor1 = Vendor(name="Vendor 1", customer=customer1)
        vendor2 = Vendor(name="Vendor 2", customer=customer2)
        db.add_all([vendor1, vendor2])

        # Create some test devices
        device1 = Device(name="Device 1", type="Router", vendor=vendor1)
        device2 = Device(name="Device 2", type="Switch", vendor=vendor2)
        db.add_all([device1, device2])

        # Create some test log entries
        severities = list(SeverityEnum)
        now = datetime.utcnow()
        for i in range(50):  # Create 50 log entries
            log = LogEntry(
                message=f"Test log {i+1}",
                severity=random.choice(severities),
                device=random.choice([device1, device2]),
                timestamp=now - timedelta(minutes=random.randint(1, 1440))  # Random time within last 24 hours
            )
            db.add(log)

        # Add a test changelog entry
        changelog_entry = ChangelogEntry(
            version="1.0.0",
            changes=json.dumps([
                {"type": "added", "description": "Initial release of the log management system."}
            ])
        )
        db.add(changelog_entry)

        db.commit()
        print("Database populated successfully.")
    except IntegrityError as e:
        print(f"An integrity error occurred while populating the database: {e}")
        db.rollback()
    except Exception as e:
        print(f"An error occurred while populating the database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    populate_db()

