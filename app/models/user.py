# User profile model for the e-commerce application
from typing import List, Dict, Any, Optional
from .base import BaseModel

class UserProfile(BaseModel):
    """User profile model for storing user information and preferences."""
    
    user_id: str
    name: Optional[str] = None
    email: Optional[str] = None
    preferences: List[str] = []
    budget_range: Optional[str] = None
    purchase_history: List[Dict[str, Any]] = []
    conversation_history: List[Dict[str, str]] = []
    
    class Config:
        # Allow extra fields for flexibility
        extra = "allow" 