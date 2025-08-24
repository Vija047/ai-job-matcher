@echo off
echo 🚀 Setting up Production AI Job Matcher Backend...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%v in ('python --version 2^>^&1') do set python_version=%%v
echo 📍 Python version: %python_version%

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo 📦 Installing Python packages...
pip install -r requirements.txt

REM Download spaCy English model
echo 🔤 Downloading spaCy English model...
python -m spacy download en_core_web_sm

REM Download NLTK data
echo 📚 Downloading NLTK data...
python -c "import nltk; import ssl; ssl._create_default_https_context = ssl._create_unverified_context; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True); nltk.download('averaged_perceptron_tagger', quiet=True); print('✅ NLTK data downloaded successfully')"

REM Create necessary directories
echo 📁 Creating directories...
if not exist "uploads" mkdir uploads
if not exist "logs" mkdir logs

REM Copy environment template if .env doesn't exist
if not exist ".env" (
    echo ⚙️  Creating environment configuration...
    copy .env.example .env
    echo 📝 Please edit .env file with your API keys and configuration
)

REM Run basic tests
echo 🧪 Running basic tests...
python -c "import sys; sys.path.append('.'); from advanced_resume_parser import AdvancedResumeParser; print('✅ Advanced Resume Parser: OK')" 2>nul || echo ❌ Advanced Resume Parser: Error
python -c "import sys; sys.path.append('.'); from job_api_client import JobAPIClient; print('✅ Job API Client: OK')" 2>nul || echo ❌ Job API Client: Error
python -c "import sys; sys.path.append('.'); from ai_job_matcher import AIJobMatcher; print('✅ AI Job Matcher: OK')" 2>nul || echo ❌ AI Job Matcher: Error
python -c "import sys; sys.path.append('.'); from auth import AuthManager; print('✅ Authentication Manager: OK')" 2>nul || echo ❌ Authentication Manager: Error

echo.
echo 🎉 Setup completed successfully!
echo.
echo 📋 Next steps:
echo 1. Edit .env file with your API keys:
echo    - ADZUNA_APP_ID and ADZUNA_APP_KEY
echo    - RAPIDAPI_KEY for JSearch API
echo    - JWT_SECRET_KEY for authentication
echo.
echo 2. Optional: Set up Redis for caching and rate limiting:
echo    - Install Redis for Windows or use Docker
echo    - Update REDIS_URL in .env
echo.
echo 3. Start the development server:
echo    python app.py
echo.
echo 4. Or start with gunicorn for production:
echo    pip install gunicorn
echo    gunicorn -w 4 -b 0.0.0.0:5000 app:app
echo.
echo 5. View API documentation:
echo    python api_docs.py (runs on port 8080)
echo.
echo 📊 API Endpoints will be available at:
echo    Health Check: http://localhost:5000/health
echo    Register: http://localhost:5000/auth/register
echo    Login: http://localhost:5000/auth/login
echo    Upload Resume: http://localhost:5000/upload-resume
echo    Search Jobs: http://localhost:5000/search-jobs
echo    Match Jobs: http://localhost:5000/match-jobs
echo.
echo 🔗 API Documentation: http://localhost:8080/docs/html
echo.
echo ⚠️  Important: Configure your API keys in .env before starting!
echo ✅ Setup complete!
pause
