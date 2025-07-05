#!/bin/bash

# Agent-Powered E-Commerce Application Runner
echo "🚀 Starting Agent-Powered E-Commerce Application..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "📝 Please create a .env file with your API keys:"
    echo "   GROQ_API_KEY=your_groq_api_key_here"
    echo "   NEO4J_URI=bolt://localhost:7687"
    echo "   NEO4J_USER=neo4j"
    echo "   NEO4J_PASSWORD=your_neo4j_password"
    echo ""
    echo "🔄 Starting with default configuration..."
fi

# Start the application
echo "🌟 Starting FastAPI server..."
echo "📱 API will be available at: http://localhost:8000"
echo "📚 API documentation at: http://localhost:8000/docs"
echo "🔍 Health check at: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the FastAPI application
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
