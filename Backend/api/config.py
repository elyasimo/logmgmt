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
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Database connection string
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://loguser:logpassword@db:5432/logdb")

# LDAP configuration
LDAP_SERVER = os.getenv("LDAP_SERVER", "ldap://your_ldap_server")

# Active Directory configuration
AD_SERVER = os.getenv("AD_SERVER", "ldap://your_ad_server")
AD_DOMAIN = os.getenv("AD_DOMAIN", "your_domain")

# SSO configuration (Google OAuth)
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

# Azure AD configuration
AZURE_AD_CLIENT_ID = os.getenv("AZURE_AD_CLIENT_ID")
AZURE_AD_CLIENT_SECRET = os.getenv("AZURE_AD_CLIENT_SECRET")
AZURE_AD_TENANT_ID = os.getenv("AZURE_AD_TENANT_ID")

