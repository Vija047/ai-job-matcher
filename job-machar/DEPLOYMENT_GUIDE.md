# 🚀 Vercel Deployment Guide for AI Job Matcher

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Vercel CLI**: Install globally with `npm install -g vercel`
3. **Git Repository**: Push your code to GitHub, GitLab, or Bitbucket

## Automated Deployment

### Option 1: Using Deploy Script (Recommended)

**Windows:**
```bash
./deploy.bat
```

**Mac/Linux:**
```bash
chmod +x deploy.sh
./deploy.sh
```

### Option 2: Manual Deployment

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm install -g vercel
   ```

2. **Build the project**:
   ```bash
   npm run build
   ```

3. **Deploy to Vercel**:
   ```bash
   vercel --prod
   ```

4. **Follow the prompts**:
   - Link to existing project or create new one
   - Choose your preferred settings

## Environment Variables Setup

After deployment, configure these environment variables in your Vercel dashboard:

### Required Variables

1. **SECRET_KEY**: `your-super-secret-key-here`
2. **NEXT_PUBLIC_API_URL**: `https://your-app-name.vercel.app/api`
3. **NEXT_PUBLIC_FRONTEND_URL**: `https://your-app-name.vercel.app`

### Optional API Keys (for enhanced features)

4. **RAPIDAPI_KEY**: Your RapidAPI key for job search APIs
5. **WELLFOUND_API_KEY**: Wellfound (AngelList) API key
6. **LINKEDIN_ACCESS_TOKEN**: LinkedIn API access token

### How to Set Environment Variables

1. Go to your [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your project
3. Go to **Settings** → **Environment Variables**
4. Add each variable with its value
5. Deploy again to apply changes

## Project Structure for Vercel

```
├── api/                    # Serverless API functions
│   ├── app.py             # Main API handler (simplified for Vercel)
│   └── index.py           # API router
├── src/                   # Next.js frontend
├── public/                # Static assets
├── backend/               # Original backend (for reference)
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies
├── package.json          # Node.js dependencies
└── next.config.mjs       # Next.js configuration
```

## Features Available in Deployed Version

✅ **Working Features:**
- Resume upload and parsing (PDF & text)
- Basic skill extraction
- Job search with mock data
- Job recommendations
- Compatibility scoring
- Responsive UI

⚠️ **Limited Features (Mock Data):**
- Real-time job scraping (uses mock data)
- External API integrations (requires API keys)
- Advanced AI features (simplified for serverless)

## Testing Your Deployment

1. **Frontend**: Visit your Vercel URL
2. **API Health**: Visit `https://your-app.vercel.app/api/health`
3. **Upload Resume**: Test the resume upload feature
4. **Job Search**: Try searching for jobs

## Troubleshooting

### Common Issues

1. **Build Failures**:
   - Check package.json for correct scripts
   - Ensure all dependencies are listed
   - Check for syntax errors

2. **API Errors**:
   - Verify environment variables are set
   - Check API function logs in Vercel dashboard
   - Ensure Python dependencies are in requirements.txt

3. **CORS Issues**:
   - API is configured to allow all origins
   - Check browser console for specific errors

### Getting Help

- Check Vercel logs in the dashboard
- Review build logs for specific errors
- Test locally first with `npm run dev`

## Scaling and Production Considerations

### Performance Optimization

1. **Cold Starts**: First API call may be slower (serverless limitation)
2. **Memory Usage**: Optimized for Vercel's memory limits
3. **Timeout**: API calls have 60-second timeout

### Adding Real APIs

To use real job search APIs:

1. Get API keys from providers (RapidAPI, Wellfound, LinkedIn)
2. Add keys to Vercel environment variables
3. Update the job search functions in `api/app.py`

### Database Integration

For persistent data storage:
1. Consider Vercel's KV storage
2. Or integrate with external databases (MongoDB Atlas, PostgreSQL)
3. Update the caching mechanism in the API

## Next Steps

1. **Custom Domain**: Configure in Vercel settings
2. **Analytics**: Add Vercel Analytics
3. **Monitoring**: Set up error tracking
4. **API Enhancement**: Integrate real job APIs
5. **Database**: Add persistent storage

## Support

- Vercel Documentation: [vercel.com/docs](https://vercel.com/docs)
- Next.js Documentation: [nextjs.org/docs](https://nextjs.org/docs)
- Project Issues: Check the GitHub repository

---

🎉 **Congratulations!** Your AI Job Matcher is now live on Vercel!
