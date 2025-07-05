from groq import Groq
import json
from typing import Dict, Any, Optional
from .config import settings

class GroqClient:
    """Client for interacting with Groq API to access LLaMA models."""
    
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.model = settings.GROQ_MODEL
        self.client = None
        
        if self.api_key:
            self.client = Groq(api_key=self.api_key)
    
    async def chat_completion(
        self, 
        messages: list, 
        temperature: float = 0.7,
        max_tokens: int = 1000,
        stream: bool = False
    ) -> Optional[Dict[str, Any]]:
        """
        Send a chat completion request to Groq API.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Controls randomness (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response
            
        Returns:
            API response or None if error
        """
        if not self.client:
            raise ValueError("GROQ_API_KEY not configured")
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream,
                top_p=1,
                stop=None
            )
            
            if stream:
                # Handle streaming response
                return self._handle_stream_response(completion)
            else:
                # Handle non-streaming response
                return {
                    "choices": [{
                        "message": {
                            "content": completion.choices[0].message.content
                        }
                    }]
                }
                
        except Exception as e:
            print(f"Error calling Groq API: {e}")
            return {"choices": [{"message": {"content": "Error processing request"}}]}
    
    def _handle_stream_response(self, completion) -> Dict[str, Any]:
        """Handle streaming response from Groq API."""
        try:
            # For now, collect the full response
            # In a real implementation, you might want to yield chunks
            full_content = ""
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_content += chunk.choices[0].delta.content
            
            return {
                "choices": [{
                    "message": {
                        "content": full_content
                    }
                }]
            }
        except Exception as e:
            print(f"Error handling stream response: {e}")
            return {"choices": [{"message": {"content": "Error processing stream response"}}]}
    
    async def generate_agent_response(
        self, 
        user_message: str, 
        context: str = "",
        user_profile: Dict[str, Any] = None
    ) -> str:
        """
        Generate an agent response for e-commerce interactions.
        
        Args:
            user_message: The user's message
            context: Additional context about the conversation
            user_profile: User profile information from knowledge graph
            
        Returns:
            Generated response from the agent
        """
        # Build system prompt for e-commerce agent
        system_prompt = """You are an AI-powered shopping assistant for an e-commerce platform. 
        Your role is to help users find products, answer questions, and provide personalized recommendations.
        
        Guidelines:
        - Be helpful, friendly, and professional
        - Ask clarifying questions when needed
        - Provide specific product recommendations when possible
        - Consider user preferences and past behavior
        - Suggest related products or alternatives
        """
        
        if context:
            system_prompt += f"\n\nContext: {context}"
        
        if user_profile:
            system_prompt += f"\n\nUser Profile: {json.dumps(user_profile, indent=2)}"
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        response = await self.chat_completion(messages, temperature=0.7)
        
        if response and "choices" in response:
            return response["choices"][0]["message"]["content"]
        else:
            return "I apologize, but I'm having trouble processing your request right now. Please try again later."
    
    def is_configured(self) -> bool:
        """Check if the Groq client is properly configured."""
        return self.client is not None and bool(self.api_key)

# Create global client instance
groq_client = GroqClient()
