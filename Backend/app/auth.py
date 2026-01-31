"""
Authentication utilities
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from odmantic import AIOEngine, ObjectId
from app.config import settings
from app.database import get_engine
from app.models import User
import hashlib, base64

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def hash_password(password: str) -> str:
    hashed = hashlib.sha256(password.encode()).digest()
    return pwd_context.hash(base64.b64encode(hashed).decode())

def verify_password(password: str, hashed: str) -> bool:
    hashed_input = hashlib.sha256(password.encode()).digest()
    return pwd_context.verify(base64.b64encode(hashed_input).decode(), hashed)

def create_access_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

def create_refresh_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=settings.refresh_token_expire_minutes)
    payload["type"] = "refresh"
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

def verify_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    engine: AIOEngine = Depends(get_engine)
) -> User:
    payload = verify_token(credentials.credentials)
    user_id = ObjectId(payload.get("sub"))

    user = await engine.find_one(User, User.id == user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
