from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import RegisterRequest, RegisterResponse, UserResponse, LoginRequest, LoginResponse
from app.utils.password import hash_password, verify_password
from app.utils.jwt import create_access_token


async def register_user(payload: RegisterRequest) -> RegisterResponse:

    # Uniqueness checks
    if await User.find_one(User.username == payload.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username is already taken"
        )

    if await User.find_one(User.email == payload.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered"
        )

    if await User.find_one(User.phone == payload.phone):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Phone number is already registered"
        )

    # Hash password
    hashed = hash_password(payload.password)

    # Save to database
    try:
        user = User(
            username=payload.username,
            email=payload.email,
            phone=payload.phone,
            hashed_password=hashed
        )
        await user.insert()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error. Please try again."
        )

    # Generate token
    token = create_access_token({"sub": str(user.id), "email": user.email})

    return RegisterResponse(
        message="Account created successfully",
        user=UserResponse(
            id=str(user.id),
            username=user.username,
            email=user.email,
            phone=user.phone,
            created_at=user.created_at
        ),
        access_token=token
    )


async def login_user(payload: LoginRequest) -> LoginResponse:

    # Find user by email
    user = await User.find_one(User.email == payload.email)

    # Verify user and password
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Generate token
    token = create_access_token({"sub": str(user.id), "email": user.email})

    return LoginResponse(
        message="Login successful",
        access_token=token
    )