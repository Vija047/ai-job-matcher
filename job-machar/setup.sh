#!/bin/bash

# AI Job Matcher - Setup Script
echo "🚀 Setting up AI Job Matcher Application..."

# Check if we're on Windows and adjust commands accordingly
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "📋 Detected Windows environment"
    PYTHON_CMD="python"
    PIP_CMD="pip"
else
    echo "📋 Detected Unix-like environment"
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
fi

# Backend Setup
echo "📦 Setting up backend..."
cd backend

# Create virtual environment
echo "🔧 Creating Python virtual environment..."
$PYTHON_CMD -m venv venv

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install Python dependencies
echo "📥 Installing Python dependencies..."
$PIP_CMD install -r requirements.txt

# Download spaCy model
echo "🤖 Downloading spaCy English model..."
$PYTHON_CMD -m spacy download en_core_web_sm

# Download NLTK data
echo "📚 Downloading NLTK data..."
$PYTHON_CMD -c "
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
print('✅ NLTK data downloaded successfully!')
"

echo "✅ Backend setup complete!"

# Return to main directory
cd ..

# Frontend Setup
echo "📦 Setting up frontend..."

# Install Node.js dependencies
echo "📥 Installing Node.js dependencies..."
npm install

echo "✅ Frontend setup complete!"

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Start the backend: cd backend && python app.py"
echo "2. Start the frontend: npm run dev"
echo "3. Open http://localhost:3000 in your browser"
echo ""
echo "💡 Tips:"
echo "- Place your PDF resume in the data/ folder"
echo "- Backend runs on http://localhost:5000"
echo "- Frontend runs on http://localhost:3000"
echo ""
echo "🎯 Happy job matching!"
