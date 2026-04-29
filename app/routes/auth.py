from fastapi import APIRouter, HTTPException, status
from app.schemas.user import RegisterRequest, RegisterResponse, UserResponse, LoginRequest, LoginResponse
from app.models.user import User
from app.utils.password import hash_password, verify_password
from app.utils.jwt import create_access_token

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=RegisterResponse
)
async def register(payload: RegisterRequest):

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

    hashed = hash_password(payload.password)

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


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=LoginResponse
)
async def login(payload: LoginRequest):

    # Find user by email
    user = await User.find_one(User.email == payload.email)

    # Check user exists and password is correct
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Generate JWT
    token = create_access_token({"sub": str(user.id), "email": user.email})

    return LoginResponse(
        message="Login successful",
        access_token=token
    )