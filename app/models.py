from typing import List, Optional
from pydantic import BaseModel


class ChatMessage(BaseModel):
    """Model for chat messages."""
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    """Model for chat requests."""
    message: str
    conversation_history: Optional[List[ChatMessage]] = []


class ChatResponse(BaseModel):
    """Model for chat responses."""
    response: str
    conversation_id: Optional[str] = None


class HealthResponse(BaseModel):
    """Model for health check responses."""
    status: str
    message: str
