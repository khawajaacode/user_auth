from fastapi import APIRouter, status, Depends
from app.schemas.profile import ProfileSetupRequest, ProfileUpdateRequest, ProfileResponse
from app.services.profile_service import setup_profile, update_profile
from app.utils.jwt import get_current_user

router = APIRouter(prefix="/api/v1/profile", tags=["Profile"])


@router.post(
    "/setup",
    status_code=status.HTTP_201_CREATED,
    response_model=ProfileResponse
)
async def setup(payload: ProfileSetupRequest, current_user: dict = Depends(get_current_user)):
    user_id = current_user["sub"]
    return await setup_profile(user_id, payload)


@router.put(
    "/update",
    status_code=status.HTTP_200_OK,
    response_model=ProfileResponse
)
async def update(payload: ProfileUpdateRequest, current_user: dict = Depends(get_current_user)):
    user_id = current_user["sub"]
    return await update_profile(user_id, payload)