# Railway Setup Guide

## Current Status
✅ Code is pushed and Railway should now use Dockerfile instead of nixpacks
✅ Configuration files are fixed

## Steps to Complete Railway Setup:

### 1. Add PostgreSQL Database to Railway
1. Go to your Railway project: https://railway.com/project/563703fd-a78e-4626-83e0-699b8bd51258
2. Click "New" button → Select "Database" → Choose "PostgreSQL"
3. Railway will automatically create the database and inject the `DATABASE_URL` environment variable

### 2. Add Environment Variables
Go to your service settings → Variables tab, and add these variables:

```
ENVIRONMENT=production
SECRET_KEY=PyKm1N4XN-25RBXgrwcBW7tBDmUSgxtUYpf8pmzuxKs
CORS_ORIGINS=http://localhost:3000,http://localhost:8000,https://frontend-exx44qzpf-jakobs-projects-bb80ead3.vercel.app,https://frontend-sigma-lac.vercel.app
GOOGLE_CLIENT_ID=1022140656174-cu4j10hs17102f98dn0250ihm67kb63m.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=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
GOOGLE_REDIRECT_URI=https://sponteproduct-production.up.railway.app/api/oauth/google/callback
CLERK_PUBLISHABLE_KEY=pk_test_aW1tdW5lLXN1bmZpc2gtNTUuY2xlcmsuYWNjb3VudHMuZGV2JA
CLERK_SECRET_KEY=sk_test_PElmNRoWmsJZUlZILClOgRhJAHMD9EfQjapmqZUliX
RESEND_API_KEY=re_UfpgPz28_9PYVSPWfMzosL7yagmZZ7VkB
```

### 3. Verify Deployment
After adding the database and environment variables:
1. Railway will automatically redeploy
2. Check the deployment logs in Railway dashboard
3. Once deployed, test the API at: https://sponteproduct-production.up.railway.app

### 4. Update Google OAuth Redirect URIs
Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials) and add:
- `https://sponteproduct-production.up.railway.app/api/oauth/google/callback`

### 5. Test the Full Application
- Frontend: https://frontend-exx44qzpf-jakobs-projects-bb80ead3.vercel.app
- Backend API: https://sponteproduct-production.up.railway.app
- API Docs (if enabled): https://sponteproduct-production.up.railway.app/docs

## Troubleshooting
If you still see "Application failed to respond":
1. Check Railway deployment logs for errors
2. Ensure PostgreSQL database is connected
3. Verify all environment variables are set
4. Check that the service is set to listen on port from PORT environment variable