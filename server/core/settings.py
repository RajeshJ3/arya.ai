from datetime import timedelta
from os import environ as env

SECRET_KEY = env["SECRET_KEY"]

DATABASE_URL = env["DATABASE_URL"]

BROKER_URL = env["BROKER_URL"]

TIMEZONE = "Asia/Kolkata"

# JWT settings
JWT_TOKEN_LIFETIME = timedelta(hours=24)
JWT_ALGORITHM = "HS256"
