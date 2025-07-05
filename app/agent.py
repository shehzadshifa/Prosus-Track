from typing import Dict, Any, Optional, List
from .groq_client import groq_client
from .knowledge_graph import knowledge_graph

class ECommerceAgent:
    """AI-powered shopping assistant agent."""
    
    def __init__(self):
        self.conversation_history: List[Dict[str, str]] = []
        self.current_user_id: Optional[str] = None
    
    async def initialize(self):
        """Initialize the agent and establish connections."""
        # Connect to Neo4j
        await knowledge_graph.connect()
        
        # Verify Groq client configuration
        if not groq_client.is_configured():
            print("⚠️  Warning: Groq API not properly configured")
        else:
            print("✅ Groq client configured successfully")
    
    async def process_message(
        self, 
        user_message: str, 
        user_id: str = "default_user",
        context: str = ""
    ) -> Dict[str, Any]:
        """
        Process a user message and generate a response.
        
        Args:
            user_message: The user's input message
            user_id: Unique identifier for the user
            context: Additional context for the conversation
            
        Returns:
            Dictionary containing the agent's response and metadata
        """
        self.current_user_id = user_id
        
        # Add message to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Get user profile from knowledge graph
        user_profile = await knowledge_graph.get_user_profile(user_id)
        
        # Generate context from conversation history
        conversation_context = self._build_conversation_context()
        
        # Combine context
        full_context = f"{context}\n{conversation_context}" if context else conversation_context
        
        try:
            # Generate response using Groq API
            agent_response = await groq_client.generate_agent_response(
                user_message=user_message,
                context=full_context,
                user_profile=user_profile
            )
            
            # Add agent response to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": agent_response
            })
            
            # Extract and store user preferences (placeholder logic)
            await self._extract_and_store_preferences(user_message, user_id)
            
            return {
                "response": agent_response,
                "user_id": user_id,
                "user_profile": user_profile,
                "conversation_length": len(self.conversation_history),
                "timestamp": self._get_timestamp()
            }
            
        except Exception as e:
            error_response = f"I apologize, but I encountered an error: {str(e)}"
            return {
                "response": error_response,
                "user_id": user_id,
                "error": str(e),
                "timestamp": self._get_timestamp()
            }
    
    def _build_conversation_context(self) -> str:
        """Build context from recent conversation history."""
        if len(self.conversation_history) <= 2:
            return ""
        
        # Get last few exchanges for context
        recent_messages = self.conversation_history[-6:]  # Last 3 exchanges
        context_parts = []
        
        for msg in recent_messages:
            role = "User" if msg["role"] == "user" else "Assistant"
            context_parts.append(f"{role}: {msg['content']}")
        
        return "\n".join(context_parts)
    
    async def _extract_and_store_preferences(self, user_message: str, user_id: str):
        """Extract user preferences from messages and store in knowledge graph."""
        # This is a placeholder implementation
        # In a real system, you would use NLP to extract preferences
        
        # Simple keyword-based preference extraction
        preferences = {
            "electronics": ["phone", "laptop", "computer", "gadget", "tech"],
            "clothing": ["shirt", "dress", "shoes", "jacket", "fashion"],
            "books": ["book", "novel", "reading", "author"],
            "sports": ["fitness", "exercise", "sports", "workout"]
        }
        
        user_message_lower = user_message.lower()
        
        for category, keywords in preferences.items():
            for keyword in keywords:
                if keyword in user_message_lower:
                    await knowledge_graph.add_user_preference(
                        user_id=user_id,
                        category=category,
                        preference=keyword
                    )
                    break
    
    async def get_user_recommendations(self, user_id: str) -> List[Dict[str, Any]]:
        """Get personalized recommendations for the user."""
        return await knowledge_graph.get_user_recommendations(user_id)
    
    async def create_user_profile(self, user_id: str, profile_data: Dict[str, Any]) -> bool:
        """Create or update a user profile."""
        return await knowledge_graph.create_or_update_user_profile(user_id, profile_data)
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the current conversation history."""
        return self.conversation_history.copy()
    
    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.conversation_history.clear()
    
    def _get_timestamp(self) -> str:
        """Get current timestamp as string."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    async def cleanup(self):
        """Clean up resources."""
        await knowledge_graph.close()

# Create global agent instance
agent = ECommerceAgent()
