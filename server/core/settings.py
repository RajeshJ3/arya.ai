from datetime import timedelta

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

DATABASE_URL = "sqlite:///sqlite.db"
BROKER_URL = "redis://localhost:6379/0"

TIMEZONE = "Asia/Kolkata"

# JWT settings
JWT_TOKEN_LIFETIME = timedelta(hours=24)
JWT_ALGORITHM = "HS256"
