# Conversation model for the e-commerce application
from typing import List, Dict, Any, Optional
from datetime import datetime
from .base import BaseModel

class Conversation(BaseModel):
    """Conversation model for storing chat interactions."""
    
    conversation_id: str
    user_id: str
    messages: List[Dict[str, str]] = []
    context: Optional[str] = None
    session_start: datetime
    session_end: Optional[datetime] = None
    intent: Optional[str] = None
    sentiment: Optional[str] = None
    
    class Config:
        # Allow extra fields for flexibility
        extra = "allow" 