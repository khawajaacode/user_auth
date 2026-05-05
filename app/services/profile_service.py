from fastapi import HTTPException, status
from datetime import datetime
from app.models.profile import Profile
from app.schemas.profile import ProfileSetupRequest, ProfileUpdateRequest, ProfileResponse


async def setup_profile(user_id: str, payload: ProfileSetupRequest) -> ProfileResponse:

    # Check if profile already exists
    existing = await Profile.find_one(Profile.user_id == user_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Profile already exists. Use update instead."
        )

    # Save profile
    profile = Profile(
        user_id=user_id,
        gender=payload.gender,
        age=payload.age,
        weight=payload.weight,
        height=payload.height,
        goal=payload.goal,
        activity_level=payload.activity_level
    )
    await profile.insert()

    return ProfileResponse(
        user_id=profile.user_id,
        gender=profile.gender,
        age=profile.age,
        weight=profile.weight,
        height=profile.height,
        goal=profile.goal,
        activity_level=profile.activity_level,
        created_at=profile.created_at,
        updated_at=profile.updated_at
    )


async def update_profile(user_id: str, payload: ProfileUpdateRequest) -> ProfileResponse:

    # Find existing profile
    profile = await Profile.find_one(Profile.user_id == user_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found. Setup profile first."
        )

    # Update only provided fields
    if payload.gender is not None:
        profile.gender = payload.gender
    if payload.age is not None:
        profile.age = payload.age
    if payload.weight is not None:
        profile.weight = payload.weight
    if payload.height is not None:
        profile.height = payload.height
    if payload.goal is not None:
        profile.goal = payload.goal
    if payload.activity_level is not None:
        profile.activity_level = payload.activity_level

    profile.updated_at = datetime.utcnow()
    await profile.save()

    return ProfileResponse(
        user_id=profile.user_id,
        gender=profile.gender,
        age=profile.age,
        weight=profile.weight,
        height=profile.height,
        goal=profile.goal,
        activity_level=profile.activity_level,
        created_at=profile.created_at,
        updated_at=profile.updated_at
    )