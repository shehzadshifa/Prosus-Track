import os
from typing import Dict, List, Optional, Any
import json
from .config import settings

try:
    from serpapi import GoogleSearch
    SERP_AVAILABLE = True
except ImportError:
    SERP_AVAILABLE = False
    print("⚠️  Warning: serpapi not installed. Using mock data only.")

class SerpApiService:
    def __init__(self):
        self.api_key = settings.SERP_API_KEY
        if not self.api_key:
            print("⚠️  Warning: SERP_API_KEY not found in environment variables")
            print("   Some features will use mock data")
    
    def search_restaurants(self, query: str, location: str = "New York") -> List[Dict]:
        """Search for restaurants using Google Search API"""
        if not self.api_key:
            return self._get_mock_restaurants()
        
        try:
            search = GoogleSearch({
                "q": f"{query} restaurants {location}",
                "api_key": self.api_key,
                "engine": "google",
                "num": 10
            })
            results = search.get_dict()
            
            restaurants = []
            if "organic_results" in results:
                for result in results["organic_results"][:10]:
                    restaurants.append({
                        "id": result.get("position", 0),
                        "name": result.get("title", "").split(" - ")[0],
                        "cuisine": query,
                        "rating": 4.2,  # Mock rating
                        "deliveryTime": "25-35 min",
                        "minOrder": 15,
                        "image": "https://via.placeholder.com/300x200?text=Restaurant",
                        "address": result.get("snippet", ""),
                        "website": result.get("link", "")
                    })
            
            return restaurants
        except Exception as e:
            print(f"Error searching restaurants: {e}")
            return self._get_mock_restaurants()
    
    def search_flights(self, from_location: str, to_location: str, date: str) -> List[Dict]:
        """Search for flights using Google Flights API"""
        if not self.api_key:
            return self._get_mock_flights()
        
        try:
            search = GoogleSearch({
                "engine": "google_flights",
                "api_key": self.api_key,
                "departure_id": from_location,
                "arrival_id": to_location,
                "outbound_date": date,
                "return_date": "",
                "adults": 1,
                "children": 0,
                "infants": 0,
                "currency": "USD"
            })
            results = search.get_dict()
            
            flights = []
            if "flights_results" in results:
                for flight in results["flights_results"][:10]:
                    flights.append({
                        "id": flight.get("flight_id", "flight_1"),
                        "airline": flight.get("airline", "Unknown"),
                        "departure": from_location,
                        "arrival": to_location,
                        "departureTime": flight.get("departure_time", "10:00 AM"),
                        "arrivalTime": flight.get("arrival_time", "2:00 PM"),
                        "price": flight.get("price", 299),
                        "duration": flight.get("duration", "4h 0m")
                    })
            
            return flights
        except Exception as e:
            print(f"Error searching flights: {e}")
            return self._get_mock_flights()
    
    def search_hotels(self, location: str, check_in: str, check_out: str) -> List[Dict]:
        """Search for hotels using Google Hotels API"""
        if not self.api_key:
            return self._get_mock_hotels()
        
        try:
            search = GoogleSearch({
                "engine": "google_hotels",
                "api_key": self.api_key,
                "q": f"hotels in {location}",
                "check_in": check_in,
                "check_out": check_out,
                "adults": 2,
                "children": 0,
                "currency": "USD"
            })
            results = search.get_dict()
            
            hotels = []
            if "hotels_results" in results:
                for hotel in results["hotels_results"][:10]:
                    hotels.append({
                        "id": hotel.get("hotel_id", "hotel_1"),
                        "name": hotel.get("title", "Hotel Name"),
                        "location": location,
                        "rating": hotel.get("rating", 4.0),
                        "price": hotel.get("price", 150),
                        "amenities": ["WiFi", "Pool", "Gym"],
                        "image": "https://via.placeholder.com/300x200?text=Hotel"
                    })
            
            return hotels
        except Exception as e:
            print(f"Error searching hotels: {e}")
            return self._get_mock_hotels()
    
    def search_products(self, query: str, category: str = None) -> List[Dict]:
        """Search for products using Google Shopping API"""
        if not self.api_key:
            return self._get_mock_products()
        
        try:
            search = GoogleSearch({
                "engine": "google_shopping",
                "api_key": self.api_key,
                "q": query,
                "num": 20
            })
            results = search.get_dict()
            
            products = []
            if "shopping_results" in results:
                for product in results["shopping_results"][:10]:
                    products.append({
                        "id": product.get("product_id", "product_1"),
                        "name": product.get("title", "Product Name"),
                        "description": product.get("description", "Product description"),
                        "price": product.get("price", 99.99),
                        "category": category or "General",
                        "condition": "new",
                        "seller": "Online Store",
                        "image": product.get("thumbnail", "https://via.placeholder.com/300x200?text=Product")
                    })
            
            return products
        except Exception as e:
            print(f"Error searching products: {e}")
            return self._get_mock_products()
    
    def _get_mock_restaurants(self) -> List[Dict]:
        """Mock restaurant data for demo"""
        return [
            {
                "id": "rest_1",
                "name": "Pizza Palace",
                "cuisine": "Pizza",
                "rating": 4.5,
                "deliveryTime": "25-35 min",
                "minOrder": 15,
                "image": "https://via.placeholder.com/300x200?text=Pizza+Palace"
            },
            {
                "id": "rest_2", 
                "name": "Sushi Express",
                "cuisine": "Sushi",
                "rating": 4.3,
                "deliveryTime": "30-45 min",
                "minOrder": 20,
                "image": "https://via.placeholder.com/300x200?text=Sushi+Express"
            },
            {
                "id": "rest_3",
                "name": "Burger House",
                "cuisine": "Burgers", 
                "rating": 4.1,
                "deliveryTime": "20-30 min",
                "minOrder": 12,
                "image": "https://via.placeholder.com/300x200?text=Burger+House"
            }
        ]
    
    def _get_mock_flights(self) -> List[Dict]:
        """Mock flight data for demo"""
        return [
            {
                "id": "flight_1",
                "airline": "Delta Airlines",
                "departure": "JFK",
                "arrival": "LAX", 
                "departureTime": "10:00 AM",
                "arrivalTime": "2:00 PM",
                "price": 299,
                "duration": "4h 0m"
            },
            {
                "id": "flight_2",
                "airline": "American Airlines",
                "departure": "JFK",
                "arrival": "LAX",
                "departureTime": "2:00 PM", 
                "arrivalTime": "6:00 PM",
                "price": 349,
                "duration": "4h 0m"
            }
        ]
    
    def _get_mock_hotels(self) -> List[Dict]:
        """Mock hotel data for demo"""
        return [
            {
                "id": "hotel_1",
                "name": "Grand Hotel",
                "location": "New York",
                "rating": 4.5,
                "price": 200,
                "amenities": ["WiFi", "Pool", "Gym", "Spa"],
                "image": "https://via.placeholder.com/300x200?text=Grand+Hotel"
            },
            {
                "id": "hotel_2",
                "name": "Comfort Inn",
                "location": "New York", 
                "rating": 4.0,
                "price": 150,
                "amenities": ["WiFi", "Breakfast"],
                "image": "https://via.placeholder.com/300x200?text=Comfort+Inn"
            }
        ]
    
    def _get_mock_products(self) -> List[Dict]:
        """Mock product data for demo"""
        return [
            {
                "id": "product_1",
                "name": "iPhone 15 Pro",
                "description": "Latest iPhone with advanced features",
                "price": 999.99,
                "category": "Electronics",
                "condition": "new",
                "seller": "Apple Store",
                "image": "https://via.placeholder.com/300x200?text=iPhone+15+Pro"
            },
            {
                "id": "product_2",
                "name": "Nike Air Max",
                "description": "Comfortable running shoes",
                "price": 129.99,
                "category": "Fashion",
                "condition": "new", 
                "seller": "Nike Store",
                "image": "https://via.placeholder.com/300x200?text=Nike+Air+Max"
            }
        ]

# Initialize the service
serp_api = SerpApiService() 