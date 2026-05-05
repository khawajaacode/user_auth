from beanie import Document
from pydantic import Field
from typing import Optional
from datetime import datetime


class Profile(Document):
    user_id: str
    gender: str
    age: int
    weight: float
    height: float
    goal: str
    activity_level: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "profiles"
        indexes = [
            [("user_id", 1)],
        ]