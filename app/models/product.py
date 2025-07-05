# Product model for the e-commerce application
from typing import List, Dict, Any, Optional
from .base import BaseModel

class Product(BaseModel):
    """Product model for storing product information."""
    
    product_id: str
    name: str
    description: Optional[str] = None
    category: str
    price: float
    currency: str = "USD"
    tags: List[str] = []
    attributes: Dict[str, Any] = {}
    availability: bool = True
    rating: Optional[float] = None
    review_count: int = 0
    
    class Config:
        # Allow extra fields for flexibility
        extra = "allow" 