from beanie import Document
from pydantic import Field
from datetime import datetime

class OTP(Document):
    email: str
    otp_code: str
    is_verified: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "otps"
        indexes = [
            [("email", 1)],
        ]