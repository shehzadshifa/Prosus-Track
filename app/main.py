from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import uvicorn

from .config import settings
from .agent import agent
from .knowledge_graph import knowledge_graph
from .groq_client import groq_client

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered e-commerce shopping assistant"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class ChatRequest(BaseModel):
    message: str
    user_id: str = "default_user"
    context: str = ""

class ChatResponse(BaseModel):
    response: str
    user_id: str
    user_profile: Optional[Dict[str, Any]] = None
    conversation_length: int
    timestamp: str
    error: Optional[str] = None

class UserProfileRequest(BaseModel):
    user_id: str
    profile_data: Dict[str, Any]

class RecommendationResponse(BaseModel):
    user_id: str
    recommendations: List[Dict[str, Any]]

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize the agent on startup."""
    print("🚀 Starting Agent-Powered E-Commerce Application...")
    await agent.initialize()
    print("✅ Application startup complete!")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    print("🛑 Shutting down application...")
    await agent.cleanup()
    print("✅ Application shutdown complete!")

# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint with basic info."""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "groq_configured": groq_client.is_configured(),
        "neo4j_connected": knowledge_graph.is_connected()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

# Main chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """
    Chat with the AI-powered shopping assistant.
    
    This endpoint processes user messages and returns personalized responses
    based on the user's profile and conversation history.
    """
    try:
        # Process the message through the agent
        result = await agent.process_message(
            user_message=request.message,
            user_id=request.user_id,
            context=request.context
        )
        
        return ChatResponse(**result)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing message: {str(e)}"
        )

# User profile management endpoints
@app.post("/user/profile")
async def create_user_profile(request: UserProfileRequest):
    """Create or update a user profile in the knowledge graph."""
    try:
        success = await agent.create_user_profile(
            user_id=request.user_id,
            profile_data=request.profile_data
        )
        
        if success:
            return {"message": "User profile created/updated successfully", "user_id": request.user_id}
        else:
            raise HTTPException(status_code=500, detail="Failed to create user profile")
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating user profile: {str(e)}"
        )

@app.get("/user/{user_id}/profile")
async def get_user_profile(user_id: str):
    """Get user profile from the knowledge graph."""
    try:
        profile = await knowledge_graph.get_user_profile(user_id)
        
        if profile:
            return {"user_id": user_id, "profile": profile}
        else:
            return {"user_id": user_id, "profile": None, "message": "User profile not found"}
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving user profile: {str(e)}"
        )

# Recommendations endpoint
@app.get("/user/{user_id}/recommendations", response_model=RecommendationResponse)
async def get_user_recommendations(user_id: str):
    """Get personalized recommendations for a user."""
    try:
        recommendations = await agent.get_user_recommendations(user_id)
        
        return RecommendationResponse(
            user_id=user_id,
            recommendations=recommendations
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting recommendations: {str(e)}"
        )

# Conversation history endpoint
@app.get("/conversation/history")
async def get_conversation_history():
    """Get the current conversation history."""
    try:
        history = agent.get_conversation_history()
        return {"conversation_history": history}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving conversation history: {str(e)}"
        )

@app.delete("/conversation/history")
async def clear_conversation_history():
    """Clear the conversation history."""
    try:
        agent.clear_conversation_history()
        return {"message": "Conversation history cleared successfully"}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error clearing conversation history: {str(e)}"
        )

# API documentation endpoint
@app.get("/docs")
async def get_api_docs():
    """Get API documentation."""
    return {
        "endpoints": {
            "POST /chat": "Chat with the AI shopping assistant",
            "POST /user/profile": "Create or update user profile",
            "GET /user/{user_id}/profile": "Get user profile",
            "GET /user/{user_id}/recommendations": "Get personalized recommendations",
            "GET /conversation/history": "Get conversation history",
            "DELETE /conversation/history": "Clear conversation history",
            "GET /health": "Health check",
            "GET /": "Application info"
        },
        "usage": {
            "chat_endpoint": {
                "method": "POST",
                "url": "/chat",
                "body": {
                    "message": "string (required)",
                    "user_id": "string (optional, default: 'default_user')",
                    "context": "string (optional)"
                }
            }
        }
    }

# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
