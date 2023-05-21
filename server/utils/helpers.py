from typing import Any

from cryptography.hazmat.primitives import serialization
from cryptography.x509 import load_pem_x509_certificate

# custom
from server.core.settings import (
    SECRET_KEY,
    JWT_TOKEN_LIFETIME,
    JWT_ALGORITHM
)

from datetime import datetime
import hashlib
import jwt


def is_path(path: str, path_var) -> bool:
    try:
        path_var_name = path.split("/")[1]
        return path_var_name == path_var
    except:
        return False


def generate_jwt(sub: str) -> str:
    now = datetime.utcnow()
    payload = {
        "sub": sub,
        "iat": int(now.timestamp()),
        "exp": int((now + JWT_TOKEN_LIFETIME).timestamp())
    }
    return jwt.encode(payload=payload, key=SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_and_validate_token(token: str) -> Any:
    return jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])


def hash_password(password: str) -> str:
    i = hashlib.sha256()
    i.update(password.encode())
    return i.hexdigest()


def compare_password_hash(password: str, password_hash: str) -> bool:
    return hash_password(password) == password_hash
