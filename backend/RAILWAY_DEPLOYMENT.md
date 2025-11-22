# Railway Deployment Guide

Deploy your Sponte AI backend to Railway for production hosting.

## Prerequisites

- ✅ Code pushed to GitHub (`https://github.com/Jakobthompson15/spontebackend`)
- ✅ Supabase account with database credentials
- ✅ GitHub account

## Step 1: Sign Up for Railway

1. Go to [railway.app](https://railway.app)
2. Click "Start a New Project"
3. Click "Login with GitHub"
4. Authorize Railway to access your GitHub account

## Step 2: Create New Project from GitHub

1. On Railway dashboard, click "New Project"
2. Select "Deploy from GitHub repo"
3. You'll see a list of your GitHub repositories
4. Find and click `Jakobthompson15/spontebackend`
5. Railway will detect it's a Python project
6. Click "Deploy Now"

Railway will start building but will fail because environment variables aren't set yet. That's expected!

## Step 3: Add Environment Variables

1. Click on your project in Railway dashboard
2. Click the "Variables" tab
3. Click "New Variable" and add these one by one:

```
SUPABASE_URL=https://mtksypjvfrdskrlvunsv.supabase.co
SUPABASE_ANON_KEY=sb_publishable_z8W52S9TXyhiLHlQ1S3RcQ_KmzXEqwa
SUPABASE_SERVICE_KEY=sb_secret_VY3jX-rJcSpM7E_U0z5Pog_oXMtrkxD
DATABASE_URL=postgresql://postgres:urgxE8Jm6b08oNnK@db.mtksypjvfrdskrlvunsv.supabase.co:5432/postgres
SECRET_KEY=PyKm1N4XN-25RBXgrwcBW7tBDmUSgxtUYpf8pmzuxKs
ENVIRONMENT=production
API_V1_PREFIX=/api
CORS_ORIGINS=http://localhost:3000,http://localhost:8000,https://your-frontend-domain.com
```

**Important**: Change `ENVIRONMENT` from `development` to `production`

4. Click "Deploy" or wait for automatic redeployment

## Step 4: Add Redis Database

1. In your Railway project, click "New" button
2. Select "Database"
3. Choose "Add Redis"
4. Railway will:
   - Create a Redis instance
   - Automatically add `REDIS_URL` environment variable
   - Redeploy your app

## Step 5: Verify Deployment

1. Go to "Deployments" tab
2. Watch the build logs
3. Look for:
   ```
   Building...
   Running release command: alembic upgrade head
   Starting server...
   ✅ Database connection successful
   ```

4. If you see errors, click "View Logs" to debug

## Step 6: Get Your Production URL

1. Click "Settings" tab
2. Scroll to "Domains" section
3. Click "Generate Domain"
4. Railway will give you a URL like:
   ```
   https://spontebackend-production-xxxx.up.railway.app
   ```
5. **Save this URL!** You'll need it for the frontend.

## Step 7: Test Production API

Open terminal and test your live API:

### Health Check
```bash
curl https://spontebackend-production-xxxx.up.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-15T...",
  "service": "Sponte AI Backend"
}
```

### Root Endpoint
```bash
curl https://spontebackend-production-xxxx.up.railway.app/
```

Expected response:
```json
{
  "service": "Sponte AI Backend",
  "version": "1.0.0",
  "status": "running",
  "environment": "production",
  "docs": "disabled in production"
}
```

### Test Onboarding (Production)
```bash
curl -X POST https://spontebackend-production-xxxx.up.railway.app/api/onboarding/submit \
  -H "Content-Type": "application/json" \
  -d '{
    "email": "production-test@example.com",
    "businessName": "Production Test LLC",
    "streetAddress": "456 Railway Ave",
    "city": "San Francisco",
    "state": "CA",
    "zipCode": "94103",
    "phone": "(415) 555-5678",
    "primaryCategory": "Software Company"
  }'
```

Should return success with user_id and location_id!

## Step 8: Verify Data in Supabase

1. Go to [supabase.com](https://supabase.com)
2. Open your project
3. Go to **Table Editor**
4. Check `users` and `locations` tables
5. You should see the production test data!

## Step 9: Update CORS Origins

Now that you have your production URL, update the CORS settings:

1. In Railway, go to "Variables"
2. Edit `CORS_ORIGINS`
3. Add your frontend domain (when you deploy it to Vercel):
   ```
   CORS_ORIGINS=http://localhost:3000,https://spontebackend-production-xxxx.up.railway.app,https://your-sponte-site.vercel.app
   ```
4. Save and redeploy

## Automatic Deployments

Railway is now configured to:
- **Auto-deploy** when you push to GitHub main branch
- **Run migrations** automatically (`alembic upgrade head` in Procfile)
- **Scale** as needed (handles multiple requests)

To deploy updates:
```bash
git add .
git commit -m "Your changes"
git push origin main
```

Railway will automatically detect the push and redeploy!

## Monitoring

### View Logs
1. Railway dashboard → Click your project
2. "View Logs" button
3. See real-time server logs

### View Metrics
1. Railway dashboard → Click your project
2. "Metrics" tab
3. See CPU, memory, network usage

### Check Deployments
1. Railway dashboard → "Deployments" tab
2. See all deployment history
3. Roll back if needed

## Pricing

Railway pricing:
- **Free tier**: $5 credit/month (enough for development)
- **Hobby plan**: $5/month for starter plan
- **Pro plan**: $20/month + usage (for production)

Each deployment uses:
- **Backend service**: ~$10-15/month
- **Redis**: ~$5/month
- **Total**: ~$20-25/month

Your first customer ($149/mo) covers this 6x over!

## Troubleshooting

### Build Fails

Check "Deployments" → "View Logs" for errors:

**Missing dependencies**: Add to `requirements.txt`
**Python version error**: Railway uses Python 3.11+ by default
**Database connection error**: Check `DATABASE_URL` is correct

### Database Migrations Fail

If you see migration errors:

1. Go to Railway dashboard → Variables
2. Verify `DATABASE_URL` is exactly right
3. Check Supabase is not paused
4. Try manual migration:
   ```bash
   # In Railway shell
   alembic upgrade head
   ```

### 504 Gateway Timeout

This means the app is taking too long to start:

1. Check "View Logs" for startup errors
2. Verify database connection
3. Check if Supabase is responsive

### CORS Errors from Frontend

If frontend can't reach API:

1. Verify `CORS_ORIGINS` includes your frontend domain
2. Check it's comma-separated with no spaces
3. Redeploy after changing

## Next Steps

After successful deployment:

1. ✅ Backend is live on Railway
2. ✅ Database migrations ran successfully
3. ✅ Redis is connected
4. ✅ API is responding

Now you can:
1. **Update frontend** (`onboarding.html`) to POST to Railway URL
2. **Test end-to-end** flow
3. **Build Phase 2**: OAuth flows and first agent!

## Support

Railway docs: https://docs.railway.app
Railway Discord: https://discord.gg/railway

If you get stuck, check Railway logs first - they're very helpful!
