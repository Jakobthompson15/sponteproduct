# Deployment Guide

This guide will help you deploy RankingMe to production.

## Overview

- **Frontend**: Deploy to Vercel (Next.js)
- **Backend**: Deploy to Railway or Render (FastAPI + PostgreSQL)
- **Database**: Supabase (already configured)

## Step 1: Deploy Backend to Railway

Railway is the easiest option for deploying FastAPI with PostgreSQL.

1. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `rankingme` repository
   - Select "backend" directory as root

3. **Configure Environment Variables**
   Add these in Railway dashboard under "Variables":
   ```
   DATABASE_URL=<your-supabase-connection-string>
   SECRET_KEY=<your-secret-key>
   CLERK_SECRET_KEY=<your-clerk-secret>
   GOOGLE_CLIENT_ID=<your-google-client-id>
   GOOGLE_CLIENT_SECRET=<your-google-client-secret>
   GOOGLE_REDIRECT_URI=https://your-app.vercel.app/oauth/google/callback
   CORS_ORIGINS=https://your-app.vercel.app
   ENCRYPTION_KEY=<your-encryption-key>
   ANTHROPIC_API_KEY=<your-anthropic-key>
   RESEND_API_KEY=<your-resend-key>
   ```

4. **Configure Build Settings**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

5. **Deploy**
   - Railway will automatically deploy
   - Note your backend URL (e.g., `https://rankingme-backend.railway.app`)

## Step 2: Deploy Frontend to Vercel

1. **Install Vercel CLI** (optional)
   ```bash
   npm install -g vercel
   ```

2. **Deploy via Vercel Dashboard**
   - Go to https://vercel.com
   - Click "New Project"
   - Import your GitHub repository
   - Select "frontend" as the root directory
   - Framework Preset: Next.js
   - Build Command: `npm run build`
   - Output Directory: `.next`

3. **Configure Environment Variables**
   Add these in Vercel dashboard under "Environment Variables":
   ```
   NEXT_PUBLIC_API_URL=https://your-backend.railway.app
   NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=<your-clerk-publishable-key>
   CLERK_SECRET_KEY=<your-clerk-secret-key>
   ```

4. **Deploy**
   - Click "Deploy"
   - Note your frontend URL (e.g., `https://rankingme.vercel.app`)

## Step 3: Update OAuth Redirect URIs

1. **Google Cloud Console**
   - Go to https://console.cloud.google.com/apis/credentials
   - Edit your OAuth 2.0 Client ID
   - Add Authorized Redirect URIs:
     ```
     https://your-app.vercel.app/oauth/google/callback
     https://your-backend.railway.app/api/oauth/google/callback
     ```

2. **Update Backend Environment**
   - In Railway, update `GOOGLE_REDIRECT_URI` to your production URL
   - Update `CORS_ORIGINS` to include your production frontend URL

3. **Update Frontend Environment**
   - In Vercel, update `NEXT_PUBLIC_API_URL` to your Railway backend URL

## Step 4: Test Production Deployment

1. Visit your Vercel URL
2. Sign up / Sign in with Clerk
3. Go through onboarding
4. Test Google OAuth connection
5. Verify GBP locations are fetched

## Alternative: Deploy Backend to Render

If you prefer Render over Railway:

1. Go to https://render.com
2. Create a new Web Service
3. Connect your GitHub repository
4. Root Directory: `backend`
5. Build Command: `pip install -r requirements.txt`
6. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
7. Add environment variables (same as Railway)

## Troubleshooting

### CORS Errors
- Ensure `CORS_ORIGINS` in backend includes your production frontend URL
- No trailing slashes in URLs

### OAuth Not Working
- Verify redirect URIs match exactly in Google Console
- Check that `GOOGLE_REDIRECT_URI` is set correctly in backend

### Database Connection Issues
- Verify Supabase connection string is correct
- Check that connection pooling is enabled
- Ensure database is accessible from Railway/Render

### Build Failures
- Check that all environment variables are set
- Verify Python version compatibility (3.11+)
- Ensure all dependencies are in requirements.txt

## Post-Deployment

1. **Request Google API Quota Increase**
   - Go to Google Cloud Console
   - Navigate to APIs & Services > Quotas
   - Request increase for My Business Account Management API
   - Provide your production URL as justification

2. **Monitor Logs**
   - Railway: Check deployment logs in dashboard
   - Vercel: Check function logs in dashboard

3. **Set up Custom Domain** (optional)
   - Vercel: Add custom domain in project settings
   - Railway: Add custom domain in service settings
