from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.models import Base
from api.config import DATABASE_URL
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    logger.info("Starting database initialization...")

    # Create tables
    Base.metadata.create_all(bind=engine)

    logger.info("Database tables created successfully.")

if __name__ == "__main__":
    init_db()

