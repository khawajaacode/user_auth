from pydantic import BaseModel
from datetime import datetime


class FeedResponse(BaseModel):
    id: str
    title: str
    description: str
    category: str
    image_url: str
    created_at: datetime