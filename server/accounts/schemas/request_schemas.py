from pydantic import BaseModel, EmailStr


class RegistrationSchema(BaseModel):
    email: EmailStr = "user@mail.com"
    first_name: str = "John"
    last_name: str = "Doe"
    password1: str = "password"
    password2: str = "password"


class LoginSchema(BaseModel):
    email: EmailStr = "user@mail.com"
    password: str = "password"
