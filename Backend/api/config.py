import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Secret key for JWT encoding/decoding
SECRET_KEY = os.getenv("SECRET_KEY", "H8md0llah_2025")

# Algorithm used for JWT encoding/decoding
ALGORITHM = "HS256"

# Access token expiration time (in minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Database connection string
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://loguser:logpassword@db:5432/logdb")

