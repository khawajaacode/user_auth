from fastapi import HTTPException, status
from datetime import datetime, timedelta
from app.models.user import User
from app.models.otp import OTP
from app.utils.email import send_otp_email
from app.utils.password import hash_password
import random
import string


def generate_otp(length: int = 6) -> str:
    return ''.join(random.choices(string.digits, k=length))


async def forgot_password(email: str):
    # Check user exists
    user = await User.find_one(User.email == email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No account found with this email"
        )

    # Delete old OTPs for this email
    await OTP.find(OTP.email == email).delete()

    # Generate new OTP
    otp_code = generate_otp()

    # Save OTP to database
    otp = OTP(email=email, otp_code=otp_code)
    await otp.insert()

    # Send email
    await send_otp_email(email, otp_code)

    return {"message": "OTP sent to your email"}


async def verify_otp(email: str, otp_code: str):
    # Find OTP
    otp = await OTP.find_one(OTP.email == email, OTP.otp_code == otp_code)

    if not otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP"
        )

    # Check expiry (5 minutes)
    expiry_time = otp.created_at + timedelta(minutes=5)
    if datetime.utcnow() > expiry_time:
        await otp.delete()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP has expired"
        )

    # Mark as verified
    otp.is_verified = True
    await otp.save()

    return {"message": "OTP verified successfully"}


async def reset_password(email: str, otp_code: str, new_password: str):
    # Check OTP is verified
    otp = await OTP.find_one(OTP.email == email, OTP.otp_code == otp_code)

    if not otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP"
        )

    if not otp.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP not verified"
        )

    # Check expiry again
    expiry_time = otp.created_at + timedelta(minutes=5)
    if datetime.utcnow() > expiry_time:
        await otp.delete()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP has expired"
        )

    # Update password
    user = await User.find_one(User.email == email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user.hashed_password = hash_password(new_password)
    await user.save()

    # Delete OTP after use
    await otp.delete()

    return {"message": "Password reset successfully"}