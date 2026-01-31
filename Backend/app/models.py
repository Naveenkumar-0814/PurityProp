"""
Database Models for Tamil Nadu Real Estate AI Assistant (MongoDB/Odmantic)
"""

from typing import List, Optional
from datetime import datetime
from odmantic import Model, EmbeddedModel, Reference, Field

class ChatMessage(EmbeddedModel):
    """Embedded chat message within a session."""
    role: str  # 'user' or 'assistant'
    content: str
    language: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class User(Model):
    """User model collection."""
    email: str = Field(unique=True, index=True)
    hashed_password: str
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ChatSession(Model):
    """Chat session model collection."""
    session_id: str = Field(unique=True, index=True)
    user: Optional[User] = None
    messages: List[ChatMessage] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
