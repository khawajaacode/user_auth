from fastapi import APIRouter, status
from app.schemas.user import RegisterRequest, RegisterResponse, LoginRequest, LoginResponse
from app.services.auth_service import register_user, login_user

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=RegisterResponse
)
async def register(payload: RegisterRequest):
    return await register_user(payload)


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=LoginResponse
)
async def login(payload: LoginRequest):
    return await login_user(payload)