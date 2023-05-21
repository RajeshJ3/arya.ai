from typing import Optional
from pydantic import BaseModel
from .model_schemas import User


class GenericResponseSchema(BaseModel):
    details: Optional[str] = None


class LoginResponseSchema(BaseModel):
    access_token: str
    user: User
