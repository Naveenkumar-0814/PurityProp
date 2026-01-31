from pydantic import BaseModel, Field, BeforeValidator
from datetime import datetime
from typing import Optional, List, Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    session_id: str = Field(..., description="Unique session identifier")
    message: str = Field(..., min_length=1, description="User message")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    session_id: str
    message: str
    language: str
    timestamp: datetime
    
    class Config:
        from_attributes = True


class SessionCreate(BaseModel):
    """Request model for creating a new session."""
    pass


class SessionResponse(BaseModel):
    """Response model for session creation."""
    session_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class MessageHistory(BaseModel):
    """Model for message in history."""
    role: str
    content: str
    language: Optional[str]
    timestamp: datetime
    
    class Config:
        from_attributes = True


class ConversationHistory(BaseModel):
    """Response model for conversation history."""
    session_id: str
    messages: List[MessageHistory]


# Authentication Schemas

class UserCreate(BaseModel):
    """Request model for user registration."""
    email: str = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password (min 8 characters)")
    name: str = Field(..., min_length=2, description="User full name")


class UserLogin(BaseModel):
    """Request model for user login."""
    email: str = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class UserResponse(BaseModel):
    """Response model for user data."""
    id: PyObjectId
    email: str
    name: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Response model for authentication token."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


class RefreshTokenRequest(BaseModel):
    """Request model for token refresh."""
    refresh_token: str
