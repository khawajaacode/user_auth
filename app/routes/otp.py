from fastapi import APIRouter, status
from pydantic import BaseModel, EmailStr
from app.services.otp_service import forgot_password, verify_otp, reset_password

router = APIRouter(prefix="/api/v1/auth", tags=["Password Reset"])


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp_code: str


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp_code: str
    new_password: str


@router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password_route(payload: ForgotPasswordRequest):
    return await forgot_password(payload.email)


@router.post("/verify-otp", status_code=status.HTTP_200_OK)
async def verify_otp_route(payload: VerifyOTPRequest):
    return await verify_otp(payload.email, payload.otp_code)


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password_route(payload: ResetPasswordRequest):
    return await reset_password(payload.email, payload.otp_code, payload.new_password)