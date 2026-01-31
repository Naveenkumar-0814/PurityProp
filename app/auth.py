"""
Authentication utilities for JWT token handling and password hashing.
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from odmantic import AIOEngine, ObjectId
from app.config import settings
from app.database import get_engine
from app.models import User

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer token scheme
security = HTTPBearer()


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt with SHA256 pre-hashing.
    Uses base64 encoding to keep the hash short and avoid bcrypt's 72-byte limit.
    """
    import hashlib
    import base64
    # Pre-hash with SHA256 and encode as base64 (44 bytes)
    password_hash = hashlib.sha256(password.encode('utf-8')).digest()
    password_b64 = base64.b64encode(password_hash).decode('utf-8')
    return pwd_context.hash(password_b64)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    Uses SHA256 pre-hashing with base64 encoding to match the hashing behavior.
    """
    import hashlib
    import base64
    # Pre-hash with SHA256 and encode as base64
    password_hash = hashlib.sha256(plain_password.encode('utf-8')).digest()
    password_b64 = base64.b64encode(password_hash).decode('utf-8')
    return pwd_context.verify(password_b64, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Data to encode in the token
        expires_delta: Optional expiration time delta
        
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT refresh token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.refresh_token_expire_minutes)
    
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


def verify_token(token: str) -> dict:
    """
    Verify and decode a JWT token.
    
    Args:
        token: JWT token to verify
        
    Returns:
        Decoded token payload
        
    Raises:
        HTTPException: If token is invalid
    """
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    engine: AIOEngine = Depends(get_engine)
) -> User:
    """
    Get the current authenticated user from JWT token.
    """
    token = credentials.credentials
    payload = verify_token(token)
    
    user_id_str: str = payload.get("sub")
    if user_id_str is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        user_id = ObjectId(user_id_str)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID format",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # Async database call
    # We can't await here easily if the dependency isn't async? 
    # FastAPI supports async dependencies.
    # But we need to use a helper or make this async.
    # Note: Logic inside async def dependency is awaited by FastAPI.
    pass

async def get_current_user_impl(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    engine: AIOEngine = Depends(get_engine)
) -> User:
    token = credentials.credentials
    payload = verify_token(token)
    
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise HTTPException(status_code=401, detail="Invalid token")
        
    try:
        user_id = ObjectId(user_id_str)
    except:
         raise HTTPException(status_code=401, detail="Invalid ID")

    user = await engine.find_one(User, User.id == user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    engine: AIOEngine = Depends(get_engine)
) -> Optional[User]:
    """
    Get the current user if authenticated, otherwise return None.
    """
    if credentials is None:
        return None
    
    try:
        return await get_current_user_impl(credentials, engine)
    except HTTPException:
        return None

# Export the async impl as the main dependency
get_current_user = get_current_user_impl
