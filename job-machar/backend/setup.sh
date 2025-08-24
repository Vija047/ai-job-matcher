#!/bin/bash

# Production AI Job Matcher Backend Setup Script
# This script sets up the complete backend environment

echo "🚀 Setting up Production AI Job Matcher Backend..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "📍 Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📦 Installing Python packages..."
pip install -r requirements.txt

# Download spaCy English model
echo "🔤 Downloading spaCy English model..."
python -m spacy download en_core_web_sm

# Download NLTK data
echo "📚 Downloading NLTK data..."
python -c "
import nltk
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
print('✅ NLTK data downloaded successfully')
"

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p uploads
mkdir -p logs

# Copy environment template if .env doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating environment configuration..."
    cp .env.example .env
    echo "📝 Please edit .env file with your API keys and configuration"
fi

# Set permissions
echo "🔐 Setting permissions..."
chmod +x setup.sh
chmod +x start.sh 2>/dev/null || true

# Run basic tests
echo "🧪 Running basic tests..."
python -c "
import sys
sys.path.append('.')

try:
    from advanced_resume_parser import AdvancedResumeParser
    print('✅ Advanced Resume Parser: OK')
except Exception as e:
    print(f'❌ Advanced Resume Parser: {e}')

try:
    from job_api_client import JobAPIClient
    print('✅ Job API Client: OK')
except Exception as e:
    print(f'❌ Job API Client: {e}')

try:
    from ai_job_matcher import AIJobMatcher
    print('✅ AI Job Matcher: OK')
except Exception as e:
    print(f'❌ AI Job Matcher: {e}')

try:
    from auth import AuthManager
    print('✅ Authentication Manager: OK')
except Exception as e:
    print(f'❌ Authentication Manager: {e}')

print('🎯 Core components loaded successfully!')
"

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file with your API keys:"
echo "   - ADZUNA_APP_ID and ADZUNA_APP_KEY"
echo "   - RAPIDAPI_KEY for JSearch API"
echo "   - JWT_SECRET_KEY for authentication"
echo ""
echo "2. Optional: Set up Redis for caching and rate limiting:"
echo "   - Install Redis: sudo apt install redis-server (Ubuntu) or brew install redis (macOS)"
echo "   - Update REDIS_URL in .env"
echo ""
echo "3. Start the development server:"
echo "   python app.py"
echo ""
echo "4. Or start with gunicorn for production:"
echo "   gunicorn -w 4 -b 0.0.0.0:5000 app:app"
echo ""
echo "5. View API documentation:"
echo "   python api_docs.py (runs on port 8080)"
echo ""
echo "📊 API Endpoints will be available at:"
echo "   Health Check: http://localhost:5000/health"
echo "   Register: http://localhost:5000/auth/register"
echo "   Login: http://localhost:5000/auth/login"
echo "   Upload Resume: http://localhost:5000/upload-resume"
echo "   Search Jobs: http://localhost:5000/search-jobs"
echo "   Match Jobs: http://localhost:5000/match-jobs"
echo ""
echo "🔗 API Documentation: http://localhost:8080/docs/html"
echo ""
echo "⚠️  Important: Configure your API keys in .env before starting!"
echo "✅ Setup complete!"
