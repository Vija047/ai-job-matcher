# 🚀 Quick Deployment Instructions

## Ready to Deploy!

Your AI Job Matcher is now configured for Vercel deployment. Here's how to deploy:

### 1. Install Vercel CLI (if not already installed)
```bash
npm install -g vercel
```

### 2. Deploy using our automated script
```bash
npm run deploy
```

**OR manually:**
```bash
vercel --prod
```

### 3. Set Environment Variables

After deployment, go to your Vercel dashboard and add these environment variables:

**Required:**
- `SECRET_KEY`: `your-super-secret-key-here`
- `NEXT_PUBLIC_API_URL`: `https://your-app-name.vercel.app/api`

**Optional (for enhanced features):**
- `RAPIDAPI_KEY`: Your RapidAPI key
- `WELLFOUND_API_KEY`: Wellfound API key
- `LINKEDIN_ACCESS_TOKEN`: LinkedIn API token

### 4. Test Your Deployment

1. Visit your Vercel URL
2. Test API health: `https://your-app.vercel.app/api/health`
3. Upload a resume and test job matching

## What's Included

✅ **Frontend & Backend** deployed as one project
✅ **Serverless API** functions for scalability
✅ **Resume parsing** (PDF & text files)
✅ **Job search** with intelligent matching
✅ **Responsive UI** works on all devices
✅ **Production optimized** build configuration

## Need Help?

- Read the full guide: `DEPLOYMENT_GUIDE.md`
- Check verification: `npm run verify`
- View logs in Vercel dashboard

---

**Ready to go live? Run:** `npm run deploy` 🚀
