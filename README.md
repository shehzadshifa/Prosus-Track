# 🤖 Agent-Powered E-Commerce Application

An AI-powered shopping assistant built with FastAPI, Groq API (LLaMA models), and Neo4j knowledge graph for personalized e-commerce experiences.

## 🚀 Features

- **AI-Powered Shopping Assistant**: Conversational interface powered by LLaMA models via Groq API
- **Knowledge Graph Storage**: User profiles and preferences stored in Neo4j
- **Personalized Recommendations**: Context-aware product suggestions
- **Modular Architecture**: Clean, extensible codebase ready for hackathon development
- **RESTful API**: FastAPI backend with comprehensive endpoints

## 🏗️ Architecture

```
agent_ecommerce/
├── app/
│   ├── main.py              # FastAPI application & endpoints
│   ├── agent.py             # AI agent orchestration logic
│   ├── groq_client.py       # Groq API integration (LLaMA models)
│   ├── knowledge_graph.py   # Neo4j knowledge graph operations
│   ├── config.py            # Environment configuration
│   └── models/              # Data models (future expansion)
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── run.sh                   # Application runner script
└── README.md               # This file
```

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **AI/LLM**: Groq API with LLaMA models
- **Database**: Neo4j (Knowledge Graph)
- **Async**: httpx for API calls
- **Configuration**: python-dotenv

## 📋 Prerequisites

1. **Python 3.8+**
2. **Neo4j Database** (local or cloud)
3. **Groq API Key** (get from [console.groq.com](https://console.groq.com/))

## ⚙️ Setup Instructions

### 1. Clone and Navigate
```bash
cd agent_ecommerce
```

### 2. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your actual values
nano .env
```

Required environment variables:
```env
# Groq API (Required)
GROQ_API_KEY=your_actual_groq_api_key

# Neo4j Database (Required)
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_neo4j_password
```

### 3. Install Dependencies
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Start Neo4j (if local)
```bash
# Using Docker
docker run -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/your_password neo4j:latest

# Or install Neo4j Desktop
```

### 5. Run the Application
```bash
# Option 1: Use the run script
./run.sh

# Option 2: Manual start
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 🌐 API Endpoints

### Core Chat Endpoint
```http
POST /chat
Content-Type: application/json

{
  "message": "I'm looking for a new laptop",
  "user_id": "user123",
  "context": "User is shopping for electronics"
}
```

### User Profile Management
```http
# Create/Update Profile
POST /user/profile
{
  "user_id": "user123",
  "profile_data": {
    "name": "John Doe",
    "preferences": ["electronics", "gaming"],
    "budget_range": "500-1000"
  }
}

# Get Profile
GET /user/{user_id}/profile

# Get Recommendations
GET /user/{user_id}/recommendations
```

### Conversation Management
```http
# Get History
GET /conversation/history

# Clear History
DELETE /conversation/history
```

### Health & Info
```http
# Application Info
GET /

# Health Check
GET /health

# API Documentation
GET /docs
```

## 🧪 Testing the API

### Using curl
```bash
# Test chat endpoint
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I need a new smartphone",
    "user_id": "test_user"
  }'

# Test health check
curl http://localhost:8000/health

# Get API documentation
curl http://localhost:8000/docs
```

### Using Python requests
```python
import requests

# Chat with the agent
response = requests.post("http://localhost:8000/chat", json={
    "message": "What laptops do you recommend?",
    "user_id": "test_user"
})
print(response.json())
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | Groq API authentication key | Required |
| `GROQ_BASE_URL` | Groq API base URL | `https://api.groq.com/openai/v1` |
| `GROQ_MODEL` | LLaMA model to use | `llama2-70b-4096` |
| `NEO4J_URI` | Neo4j database URI | `bolt://localhost:7687` |
| `NEO4J_USER` | Neo4j username | `neo4j` |
| `NEO4J_PASSWORD` | Neo4j password | Required |
| `DEBUG` | Enable debug mode | `False` |

## 🚀 Future Enhancements

### Voice Support
- Web Speech API integration
- Twilio voice capabilities
- Speech-to-text and text-to-speech

### Additional Modules
- **Travel Booking**: Flight/hotel recommendations
- **Food Ordering**: Restaurant and delivery integration
- **Product Catalog**: Dynamic product database
- **Payment Integration**: Stripe/PayPal support

### Advanced Features
- Multi-language support
- Sentiment analysis
- Advanced recommendation algorithms
- Real-time notifications

## 🐛 Troubleshooting

### Common Issues

1. **Neo4j Connection Failed**
   - Verify Neo4j is running
   - Check credentials in `.env`
   - Ensure firewall allows port 7687

2. **Groq API Errors**
   - Verify API key is correct
   - Check API quota/limits
   - Ensure internet connectivity

3. **Import Errors**
   - Activate virtual environment
   - Reinstall dependencies: `pip install -r requirements.txt`

### Debug Mode
```bash
# Enable debug logging
export DEBUG=True
python -m uvicorn app.main:app --reload
```

## 📚 API Documentation

Once the server is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 🤝 Contributing

This is a hackathon project designed for rapid development and experimentation. Feel free to:

1. Fork the repository
2. Add new features
3. Improve documentation
4. Report issues

## 📄 License

This project is open source and available under the MIT License.

---

**Happy Hacking! 🚀**
