"""
Authentication Routes

Handles user registration, login, and user info endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from odmantic import AIOEngine
from app.database import get_engine
from app.models import User
from app.schemas import UserCreate, UserLogin, Token, UserResponse, RefreshTokenRequest
from app.auth import hash_password, verify_password, create_access_token, create_refresh_token, get_current_user
from datetime import timedelta
from app.config import settings

router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, engine: AIOEngine = Depends(get_engine)):
    """
    Register a new user.
    """
    # Check if user already exists
    existing_user = await engine.find_one(User, User.email == user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        name=user_data.name
    )
    
    await engine.save(new_user)
    
    # Create tokens
    access_token = create_access_token(
        data={"sub": str(new_user.id)}
    )
    refresh_token = create_refresh_token(
        data={"sub": str(new_user.id)}
    )
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.model_validate(new_user)
    )


@router.post("/login", response_model=Token)
async def login_user(credentials: UserLogin, engine: AIOEngine = Depends(get_engine)):
    """
    Login user and return JWT tokens.
    """
    # Find user by email
    user = await engine.find_one(User, User.email == credentials.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create tokens
    access_token = create_access_token(
        data={"sub": str(user.id)}
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.id)}
    )
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.model_validate(user)
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(request: RefreshTokenRequest, engine: AIOEngine = Depends(get_engine)):
    """
    Refresh access token using refresh token.
    """
    try:
        from app.auth import verify_token
        payload = verify_token(request.refresh_token)
        
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        user_id_str = payload.get("sub")
        if not user_id_str:
            raise HTTPException(status_code=401, detail="Invalid token")
            
        # Verify user still exists
        try:
            from odmantic import ObjectId
            user_id = ObjectId(user_id_str)
        except:
            raise HTTPException(status_code=401, detail="Invalid user ID")
            
        user = await engine.find_one(User, User.id == user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
            
        # Issue new access token
        access_token = create_access_token(
            data={"sub": user_id_str}
        )
        
        # We can rotate refresh token here if we want, but keeping it simple for now
        # We return the same refresh token to keep it valid until expiry
        
        return Token(
            access_token=access_token,
            refresh_token=request.refresh_token,
            user=UserResponse.model_validate(user)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user information.
    """
    return UserResponse.model_validate(current_user)
