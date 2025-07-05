# Models package for Agent-Powered E-Commerce Application
# This package will contain data models for future expansion

from .base import BaseModel
from .user import UserProfile
from .product import Product
from .conversation import Conversation

__all__ = [
    "BaseModel",
    "UserProfile", 
    "Product",
    "Conversation"
] 