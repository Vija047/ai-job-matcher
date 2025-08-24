#!/bin/bash

# Deployment script for AI Job Matcher to Vercel
echo "🚀 Deploying AI Job Matcher to Vercel..."

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

# Build frontend
echo "📦 Building frontend..."
npm run build

# Deploy to Vercel
echo "🌐 Deploying to Vercel..."
vercel --prod

echo "✅ Deployment complete!"
echo ""
echo "📋 Post-deployment checklist:"
echo "1. Set environment variables in Vercel dashboard"
echo "2. Configure domain (optional)"
echo "3. Test API endpoints"
echo "4. Update NEXT_PUBLIC_API_URL in environment variables"
