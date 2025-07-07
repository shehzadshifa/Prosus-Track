from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import uvicorn

from .config import settings
from .agent import agent
from .knowledge_graph import knowledge_graph
from .groq_client import groq_client
from .serp_api import serp_api

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

# Food Ordering Models
class RestaurantSearchRequest(BaseModel):
    query: str
    location: str = "New York"

class OrderRequest(BaseModel):
    restaurantId: str
    items: List[Dict[str, Any]]
    deliveryAddress: str
    paymentMethod: str

# Travel Booking Models
class FlightSearchRequest(BaseModel):
    from_location: str
    to_location: str
    date: str
    passengers: int = 1

class HotelSearchRequest(BaseModel):
    location: str
    check_in: str
    check_out: str
    guests: int = 2

class FlightBookingRequest(BaseModel):
    flightId: str
    passengers: List[Dict[str, str]]
    paymentMethod: str

class HotelBookingRequest(BaseModel):
    hotelId: str
    check_in: str
    check_out: str
    guests: int
    paymentMethod: str

# Marketplace Models
class ProductSearchRequest(BaseModel):
    query: str
    category: Optional[str] = None
    condition: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None

class ProductPurchaseRequest(BaseModel):
    productId: str
    quantity: int
    shippingAddress: str
    paymentMethod: str

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

# Food Ordering Endpoints
@app.get("/food/restaurants")
async def search_restaurants(query: str, location: str = "New York"):
    """Search for restaurants using SerpApi."""
    try:
        restaurants = serp_api.search_restaurants(query, location)
        return {"restaurants": restaurants}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching restaurants: {str(e)}"
        )

@app.get("/food/restaurants/{restaurant_id}/menu")
async def get_restaurant_menu(restaurant_id: str):
    """Get restaurant menu (mock data for demo)."""
    menu_items = [
        {
            "id": "item_1",
            "name": "Margherita Pizza",
            "description": "Fresh mozzarella, tomato sauce, basil",
            "price": 18.99,
            "category": "Pizza",
            "image": "https://via.placeholder.com/200x150?text=Pizza"
        },
        {
            "id": "item_2",
            "name": "Caesar Salad",
            "description": "Romaine lettuce, parmesan, croutons",
            "price": 12.99,
            "category": "Salad",
            "image": "https://via.placeholder.com/200x150?text=Salad"
        }
    ]
    return {"menu_items": menu_items}

@app.post("/food/order")
async def place_food_order(request: OrderRequest):
    """Place a food order."""
    try:
        # Simulate order processing
        order_id = f"order_{len(request.items)}_{hash(str(request))}"
        return {
            "order_id": order_id,
            "status": "confirmed",
            "estimated_delivery": "30-45 minutes",
            "total": sum(item.get("price", 0) * item.get("quantity", 1) for item in request.items)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error placing order: {str(e)}"
        )

# Travel Booking Endpoints
@app.get("/travel/flights")
async def search_flights(
    from_location: str,
    to_location: str,
    date: str,
    passengers: int = 1
):
    """Search for flights using SerpApi."""
    try:
        flights = serp_api.search_flights(from_location, to_location, date)
        return {"flights": flights}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching flights: {str(e)}"
        )

@app.get("/travel/hotels")
async def search_hotels(
    location: str,
    check_in: str,
    check_out: str,
    guests: int = 2
):
    """Search for hotels using SerpApi."""
    try:
        hotels = serp_api.search_hotels(location, check_in, check_out)
        return {"hotels": hotels}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching hotels: {str(e)}"
        )

@app.post("/travel/flights/book")
async def book_flight(request: FlightBookingRequest):
    """Book a flight."""
    try:
        booking_id = f"flight_booking_{hash(str(request))}"
        return {
            "booking_id": booking_id,
            "status": "confirmed",
            "flight_id": request.flightId,
            "passengers": request.passengers
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error booking flight: {str(e)}"
        )

@app.post("/travel/hotels/book")
async def book_hotel(request: HotelBookingRequest):
    """Book a hotel."""
    try:
        booking_id = f"hotel_booking_{hash(str(request))}"
        return {
            "booking_id": booking_id,
            "status": "confirmed",
            "hotel_id": request.hotelId,
            "check_in": request.check_in,
            "check_out": request.check_out,
            "guests": request.guests
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error booking hotel: {str(e)}"
        )

@app.post("/travel/itinerary")
async def create_itinerary(request: Dict[str, Any]):
    """Create a travel itinerary."""
    try:
        itinerary_id = f"itinerary_{hash(str(request))}"
        return {
            "itinerary_id": itinerary_id,
            "status": "created",
            "flights": request.get("flights", []),
            "hotels": request.get("hotels", []),
            "activities": request.get("activities", [])
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating itinerary: {str(e)}"
        )

# Marketplace Endpoints
@app.get("/marketplace/products")
async def search_products(
    query: Optional[str] = None,
    category: Optional[str] = None,
    condition: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
):
    """Search for products using SerpApi."""
    try:
        products = serp_api.search_products(query or "electronics", category or "General")
        return {"products": products}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching products: {str(e)}"
        )

@app.get("/marketplace/products/{product_id}")
async def get_product(product_id: str):
    """Get product details."""
    try:
        # Mock product data
        product = {
            "id": product_id,
            "name": "iPhone 15 Pro",
            "description": "Latest iPhone with advanced features",
            "price": 999.99,
            "category": "Electronics",
            "condition": "new",
            "seller": "Apple Store",
            "image": "https://via.placeholder.com/300x200?text=iPhone+15+Pro"
        }
        return product
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting product: {str(e)}"
        )

@app.post("/marketplace/purchase")
async def purchase_product(request: ProductPurchaseRequest):
    """Purchase a product."""
    try:
        purchase_id = f"purchase_{hash(str(request))}"
        return {
            "purchase_id": purchase_id,
            "status": "confirmed",
            "product_id": request.productId,
            "quantity": request.quantity,
            "shipping_address": request.shippingAddress
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error purchasing product: {str(e)}"
        )

@app.post("/marketplace/sell")
async def sell_product(request: Dict[str, Any]):
    """List a product for sale."""
    try:
        listing_id = f"listing_{hash(str(request))}"
        return {
            "listing_id": listing_id,
            "status": "active",
            "product": request
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating listing: {str(e)}"
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
            "GET /food/restaurants": "Search restaurants",
            "GET /food/restaurants/{id}/menu": "Get restaurant menu",
            "POST /food/order": "Place food order",
            "GET /travel/flights": "Search flights",
            "GET /travel/hotels": "Search hotels",
            "POST /travel/flights/book": "Book flight",
            "POST /travel/hotels/book": "Book hotel",
            "POST /travel/itinerary": "Create itinerary",
            "GET /marketplace/products": "Search products",
            "GET /marketplace/products/{id}": "Get product details",
            "POST /marketplace/purchase": "Purchase product",
            "POST /marketplace/sell": "Sell product",
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
