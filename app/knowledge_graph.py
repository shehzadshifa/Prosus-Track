from neo4j import GraphDatabase
from typing import Dict, Any, Optional, List
from .config import settings

class KnowledgeGraph:
    """Neo4j knowledge graph for storing user profiles and preferences."""
    
    def __init__(self):
        self.driver = None
        self.uri = settings.NEO4J_URI
        self.user = settings.NEO4J_USER
        self.password = settings.NEO4J_PASSWORD
    
    async def connect(self):
        """Establish connection to Neo4j database."""
        try:
            self.driver = GraphDatabase.driver(
                self.uri, 
                auth=(self.user, self.password)
            )
            # Test the connection
            with self.driver.session() as session:
                session.run("RETURN 1")
            print("✅ Connected to Neo4j successfully")
        except Exception as e:
            print(f"❌ Failed to connect to Neo4j: {e}")
            self.driver = None
    
    async def close(self):
        """Close the Neo4j connection."""
        if self.driver:
            self.driver.close()
    
    def _create_user_profile(self, tx, user_id: str, profile_data: Dict[str, Any]):
        """Create or update user profile in Neo4j."""
        query = """
        MERGE (u:User {user_id: $user_id})
        SET u += $profile_data
        RETURN u
        """
        result = tx.run(query, user_id=user_id, profile_data=profile_data)
        return result.single()
    
    def _get_user_profile(self, tx, user_id: str):
        """Retrieve user profile from Neo4j."""
        query = """
        MATCH (u:User {user_id: $user_id})
        RETURN u
        """
        result = tx.run(query, user_id=user_id)
        return result.single()
    
    def _add_user_preference(self, tx, user_id: str, category: str, preference: str):
        """Add a user preference to the knowledge graph."""
        query = """
        MATCH (u:User {user_id: $user_id})
        MERGE (c:Category {name: $category})
        MERGE (p:Preference {value: $preference})
        MERGE (u)-[:LIKES]->(p)
        MERGE (p)-[:BELONGS_TO]->(c)
        RETURN u, c, p
        """
        result = tx.run(query, user_id=user_id, category=category, preference=preference)
        return result.data()
    
    def _add_purchase_history(self, tx, user_id: str, product_id: str, product_name: str):
        """Add purchase history to the knowledge graph."""
        query = """
        MATCH (u:User {user_id: $user_id})
        MERGE (p:Product {product_id: $product_id, name: $product_name})
        MERGE (u)-[:PURCHASED]->(p)
        RETURN u, p
        """
        result = tx.run(query, user_id=user_id, product_id=product_id, product_name=product_name)
        return result.data()
    
    async def create_or_update_user_profile(self, user_id: str, profile_data: Dict[str, Any]) -> bool:
        """Create or update a user profile in the knowledge graph."""
        if not self.driver:
            print("❌ No Neo4j connection available")
            return False
        
        try:
            with self.driver.session() as session:
                session.execute_write(self._create_user_profile, user_id, profile_data)
                print(f"✅ User profile created/updated for user: {user_id}")
                return True
        except Exception as e:
            print(f"❌ Error creating user profile: {e}")
            return False
    
    async def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve user profile from the knowledge graph."""
        if not self.driver:
            print("❌ No Neo4j connection available")
            return None
        
        try:
            with self.driver.session() as session:
                result = session.execute_read(self._get_user_profile, user_id)
                if result:
                    return dict(result["u"])
                return None
        except Exception as e:
            print(f"❌ Error retrieving user profile: {e}")
            return None
    
    async def add_user_preference(self, user_id: str, category: str, preference: str) -> bool:
        """Add a user preference to the knowledge graph."""
        if not self.driver:
            print("❌ No Neo4j connection available")
            return False
        
        try:
            with self.driver.session() as session:
                session.execute_write(self._add_user_preference, user_id, category, preference)
                print(f"✅ Added preference '{preference}' in category '{category}' for user: {user_id}")
                return True
        except Exception as e:
            print(f"❌ Error adding user preference: {e}")
            return False
    
    async def add_purchase_history(self, user_id: str, product_id: str, product_name: str) -> bool:
        """Add purchase history to the knowledge graph."""
        if not self.driver:
            print("❌ No Neo4j connection available")
            return False
        
        try:
            with self.driver.session() as session:
                session.execute_write(self._add_purchase_history, user_id, product_id, product_name)
                print(f"✅ Added purchase history for product '{product_name}' for user: {user_id}")
                return True
        except Exception as e:
            print(f"❌ Error adding purchase history: {e}")
            return False
    
    async def get_user_recommendations(self, user_id: str) -> List[Dict[str, Any]]:
        """Get personalized recommendations based on user profile and history."""
        if not self.driver:
            print("❌ No Neo4j connection available")
            return []
        
        try:
            with self.driver.session() as session:
                # This is a placeholder query - in a real implementation,
                # you would have more sophisticated recommendation logic
                query = """
                MATCH (u:User {user_id: $user_id})-[:LIKES]->(p:Preference)-[:BELONGS_TO]->(c:Category)
                RETURN c.name as category, collect(p.value) as preferences
                LIMIT 5
                """
                result = session.run(query, user_id=user_id)
                return [record.data() for record in result]
        except Exception as e:
            print(f"❌ Error getting recommendations: {e}")
            return []
    
    def is_connected(self) -> bool:
        """Check if connected to Neo4j."""
        return self.driver is not None

# Create global knowledge graph instance
knowledge_graph = KnowledgeGraph()
