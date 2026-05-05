from beanie import Document
from pydantic import Field
from datetime import datetime


class Feed(Document):
    title: str
    description: str
    category: str
    image_url: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "feeds"