@echo off
setlocal EnableDelayedExpansion

echo 🚀 Starting AI Job Matcher Development Environment...

REM Check dependencies
echo 🔍 Checking dependencies...

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

where node >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js 16+ and try again.
    pause
    exit /b 1
)

where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ npm is not installed. Please install npm and try again.
    pause
    exit /b 1
)

echo ✅ All dependencies found!

REM Check if ports are available
netstat -an | findstr ":5000 " >nul 2>nul
if %errorlevel% equ 0 (
    echo ⚠️  Port 5000 is already in use. Backend may not start properly.
)

netstat -an | findstr ":3000 " >nul 2>nul
if %errorlevel% equ 0 (
    echo ⚠️  Port 3000 is already in use. Frontend may not start properly.
)

REM Start backend
echo 🔧 Starting backend server...
cd backend

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies if needed
if not exist "venv\.dependencies_installed" (
    echo 📥 Installing Python dependencies...
    pip install -r requirements.txt
    python -m spacy download en_core_web_sm
    echo. > venv\.dependencies_installed
)

REM Start backend server
echo 🎯 Launching backend on http://localhost:5000
start /b python app.py

REM Return to main directory
cd ..

REM Install frontend dependencies if needed
if not exist "node_modules" (
    echo 📥 Installing frontend dependencies...
    npm install
)

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend
echo 🎨 Launching frontend on http://localhost:3000
start /b npm run dev

echo.
echo 🎉 AI Job Matcher is starting up!
echo 📊 Backend API: http://localhost:5000
echo 🌐 Frontend App: http://localhost:3000
echo.
echo 💡 Press any key to stop all services
echo 📝 Check the console windows for logs
echo.

pause >nul

REM Cleanup
echo 🛑 Shutting down services...
taskkill /f /im python.exe >nul 2>nul
taskkill /f /im node.exe >nul 2>nul
echo ✅ Services stopped
echo 👋 Goodbye!
pause
