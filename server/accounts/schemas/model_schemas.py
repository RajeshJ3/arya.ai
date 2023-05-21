from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: int = 1
    email: EmailStr = "user@mail.com"
    first_name: str = "John"
    last_name: str = "Doe"
