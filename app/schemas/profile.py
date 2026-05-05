from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime

VALID_GOALS = ["gain weight", "lose weight", "get fitter", "gain more flexible", "learn the basic"]
VALID_ACTIVITY_LEVELS = ["rookie", "beginner", "intermediate", "advance", "true beast"]
VALID_GENDERS = ["male", "female"]


class ProfileSetupRequest(BaseModel):
    gender: str
    age: int
    weight: float
    height: float
    goal: str
    activity_level: str

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, v: str) -> str:
        v = v.lower().strip()
        if v not in VALID_GENDERS:
            raise ValueError("Gender must be male or female")
        return v

    @field_validator("age")
    @classmethod
    def validate_age(cls, v: int) -> int:
        if v < 10 or v > 100:
            raise ValueError("Age must be between 10 and 100")
        return v

    @field_validator("weight")
    @classmethod
    def validate_weight(cls, v: float) -> float:
        if v < 20 or v > 300:
            raise ValueError("Weight must be between 20 and 300 kg")
        return v

    @field_validator("height")
    @classmethod
    def validate_height(cls, v: float) -> float:
        if v < 100 or v > 250:
            raise ValueError("Height must be between 100 and 250 cm")
        return v

    @field_validator("goal")
    @classmethod
    def validate_goal(cls, v: str) -> str:
        v = v.lower().strip()
        if v not in VALID_GOALS:
            raise ValueError(f"Goal must be one of: {VALID_GOALS}")
        return v

    @field_validator("activity_level")
    @classmethod
    def validate_activity_level(cls, v: str) -> str:
        v = v.lower().strip()
        if v not in VALID_ACTIVITY_LEVELS:
            raise ValueError(f"Activity level must be one of: {VALID_ACTIVITY_LEVELS}")
        return v


class ProfileUpdateRequest(BaseModel):
    gender: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    goal: Optional[str] = None
    activity_level: Optional[str] = None

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, v: str) -> str:
        if v is not None:
            v = v.lower().strip()
            if v not in VALID_GENDERS:
                raise ValueError("Gender must be male or female")
        return v

    @field_validator("goal")
    @classmethod
    def validate_goal(cls, v: str) -> str:
        if v is not None:
            v = v.lower().strip()
            if v not in VALID_GOALS:
                raise ValueError(f"Goal must be one of: {VALID_GOALS}")
        return v

    @field_validator("activity_level")
    @classmethod
    def validate_activity_level(cls, v: str) -> str:
        if v is not None:
            v = v.lower().strip()
            if v not in VALID_ACTIVITY_LEVELS:
                raise ValueError(f"Activity level must be one of: {VALID_ACTIVITY_LEVELS}")
        return v


class ProfileResponse(BaseModel):
    user_id: str
    gender: str
    age: int
    weight: float
    height: float
    goal: str
    activity_level: str
    created_at: datetime
    updated_at: datetime