# Base model for all data models in the application
from pydantic import BaseModel as PydanticBaseModel
from typing import Optional
from datetime import datetime

class BaseModel(PydanticBaseModel):
    """Base model with common fields for all entities."""
    
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        # Allow extra fields for flexibility
        extra = "allow" 