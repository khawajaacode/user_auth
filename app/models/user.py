from beanie import Document
from pydantic import EmailStr, Field
from datetime import datetime

class User(Document):
    username: str
    email: EmailStr
    phone: str
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"
        indexes = [
            [("username", 1)],
            [("email", 1)],
            [("phone", 1)],
        ]
