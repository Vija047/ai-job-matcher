@echo off
REM Deployment script for AI Job Matcher to Vercel (Windows)

echo 🚀 Deploying AI Job Matcher to Vercel...

REM Check if Vercel CLI is installed
where vercel >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Vercel CLI not found. Installing...
    npm install -g vercel
)

REM Build frontend
echo 📦 Building frontend...
npm run build

REM Deploy to Vercel
echo 🌐 Deploying to Vercel...
vercel --prod

echo ✅ Deployment complete!
echo.
echo 📋 Post-deployment checklist:
echo 1. Set environment variables in Vercel dashboard
echo 2. Configure domain (optional)
echo 3. Test API endpoints
echo 4. Update NEXT_PUBLIC_API_URL in environment variables

pause
