@echo off
echo Starting AI Job Matcher Application...
echo.

echo Starting Backend Server...
start "Backend" cmd /k "cd backend && python app.py"

echo Waiting for backend to initialize...
timeout /t 3 /nobreak >nul

echo Starting Frontend Server...
start "Frontend" cmd /k "npm run dev"

echo.
echo AI Job Matcher is starting...
echo Frontend: http://localhost:3001
echo Backend: http://localhost:5000
echo.
echo Press any key to continue...
pause >nul
