import os
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL Database Settings
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "sharecaredb")

# Build DATABASE_URL
DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# JWT
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OTP
OTP_EXPIRE_MINUTES = 5
OTP_LENGTH = 4

# Encryption (Fernet for phone number encryption)
FERNET_KEY = os.getenv("FERNET_KEY", "your-fernet-key-here").encode()
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "default-key-change-in-production")

# API Settings
API_TITLE = "Dobrodar API"
API_VERSION = "0.1.0"
API_DESCRIPTION = "Сервис обмена вещами между пользователями"

# CORS
ALLOWED_ORIGINS = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
]

# Upload settings
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}
UPLOAD_DIR = "uploads"