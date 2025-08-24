#!/bin/bash

# AI Job Matcher - Development Startup Script
echo "🚀 Starting AI Job Matcher Development Environment..."

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if a port is in use
port_in_use() {
    netstat -an 2>/dev/null | grep ":$1 " >/dev/null 2>&1
}

# Check dependencies
echo "🔍 Checking dependencies..."

if ! command_exists python3 && ! command_exists python; then
    echo "❌ Python is not installed. Please install Python 3.8+ and try again."
    exit 1
fi

if ! command_exists node; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ and try again."
    exit 1
fi

if ! command_exists npm; then
    echo "❌ npm is not installed. Please install npm and try again."
    exit 1
fi

echo "✅ All dependencies found!"

# Determine Python command
if command_exists python3; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

# Check if ports are available
if port_in_use 5000; then
    echo "⚠️  Port 5000 is already in use. Backend may not start properly."
fi

if port_in_use 3000; then
    echo "⚠️  Port 3000 is already in use. Frontend may not start properly."
fi

# Start backend in background
echo "🔧 Starting backend server..."
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    $PYTHON_CMD -m venv venv
fi

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies if needed
if [ ! -f "venv/.dependencies_installed" ]; then
    echo "📥 Installing Python dependencies..."
    pip install -r requirements.txt
    $PYTHON_CMD -m spacy download en_core_web_sm
    touch venv/.dependencies_installed
fi

# Start backend server
echo "🎯 Launching backend on http://localhost:5000"
$PYTHON_CMD app.py &
BACKEND_PID=$!

# Return to main directory
cd ..

# Install frontend dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📥 Installing frontend dependencies..."
    npm install
fi

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "🎨 Launching frontend on http://localhost:3000"
npm run dev &
FRONTEND_PID=$!

# Function to cleanup background processes
cleanup() {
    echo ""
    echo "🛑 Shutting down services..."
    
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        echo "✅ Backend stopped"
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        echo "✅ Frontend stopped"
    fi
    
    echo "👋 Goodbye!"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

echo ""
echo "🎉 AI Job Matcher is starting up!"
echo "📊 Backend API: http://localhost:5000"
echo "🌐 Frontend App: http://localhost:3000"
echo ""
echo "💡 Press Ctrl+C to stop all services"
echo "📝 Check the logs above for any errors"
echo ""

# Wait for background processes
wait
