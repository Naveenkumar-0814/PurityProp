"""
Authentication Routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from odmantic import AIOEngine
from app.database import get_engine
from app.models import User
from app.schemas import (
    UserCreate,
    UserLogin,
    Token,
    UserResponse,
    RefreshTokenRequest,
)
from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    get_current_user,
    verify_token,
)
from odmantic import ObjectId

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    engine: AIOEngine = Depends(get_engine)
):
    existing_user = await engine.find_one(User, User.email == user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=user_data.email,
        name=user_data.name,
        hashed_password=hash_password(user_data.password)
    )

    await engine.save(user)

    return Token(
        access_token=create_access_token({"sub": str(user.id)}),
        refresh_token=create_refresh_token({"sub": str(user.id)}),
        user=UserResponse.model_validate(user)
    )


@router.post("/login", response_model=Token)
async def login_user(
    credentials: UserLogin,
    engine: AIOEngine = Depends(get_engine)
):
    user = await engine.find_one(User, User.email == credentials.email)
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return Token(
        access_token=create_access_token({"sub": str(user.id)}),
        refresh_token=create_refresh_token({"sub": str(user.id)}),
        user=UserResponse.model_validate(user)
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(
    request: RefreshTokenRequest,
    engine: AIOEngine = Depends(get_engine)
):
    payload = verify_token(request.refresh_token)

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user_id = ObjectId(payload["sub"])
    user = await engine.find_one(User, User.id == user_id)

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return Token(
        access_token=create_access_token({"sub": str(user.id)}),
        refresh_token=request.refresh_token,
        user=UserResponse.model_validate(user)
    )


@router.get("/me", response_model=UserResponse)
async def me(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)
