# 🚀 Quick Start Guide

Get your Sponte AI backend running in 3 simple steps!

## What You Have

✅ Complete FastAPI backend (27 files, 1540+ lines of code)
✅ 5 database models (users, locations, agents, tokens, tasks)
✅ 2 API endpoints (health check + onboarding)
✅ Supabase Postgres database integration
✅ Alembic migrations ready
✅ Railway deployment config
✅ Git repository initialized

## The 3-Step Process

### Step 1: Test Locally (20 minutes)

Follow [LOCAL_SETUP_INSTRUCTIONS.md](./LOCAL_SETUP_INSTRUCTIONS.md)

Quick version:
```bash
cd /Users/jakobthompson/Desktop/personal/rankingme/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

Test: `curl http://localhost:8000/health`

### Step 2: Push to GitHub (2 minutes)

Follow [GIT_PUSH_INSTRUCTIONS.md](./GIT_PUSH_INSTRUCTIONS.md)

Quick version:
```bash
cd /Users/jakobthompson/Desktop/personal/rankingme/backend
git push -u origin main
```

### Step 3: Deploy to Railway (10 minutes)

Follow [RAILWAY_DEPLOYMENT.md](./RAILWAY_DEPLOYMENT.md)

Quick version:
1. Go to railway.app → Login with GitHub
2. New Project → Deploy from GitHub → Select `spontebackend`
3. Add environment variables (from `.env` file)
4. Add Redis database
5. Generate domain
6. Test: `curl https://your-app.railway.app/health`

## What's Next?

After deployment is successful:

1. **Update Frontend** - Connect `onboarding.html` to Railway API
2. **Test End-to-End** - Submit form → Data saves to Supabase
3. **Build Phase 2** - OAuth flows + First agent (GBP Agent)

## Need Help?

- **Local issues**: See [LOCAL_SETUP_INSTRUCTIONS.md](./LOCAL_SETUP_INSTRUCTIONS.md) troubleshooting section
- **Git issues**: See [GIT_PUSH_INSTRUCTIONS.md](./GIT_PUSH_INSTRUCTIONS.md) authentication options
- **Railway issues**: See [RAILWAY_DEPLOYMENT.md](./RAILWAY_DEPLOYMENT.md) troubleshooting section
- **General docs**: See [README.md](./README.md)

## File Overview

| File | Purpose |
|------|---------|
| `app/main.py` | FastAPI application entry point |
| `app/config.py` | Environment configuration |
| `app/database.py` | SQLAlchemy database setup |
| `app/models/` | Database models (User, Location, etc.) |
| `app/routers/` | API endpoints (health, onboarding) |
| `app/schemas/` | Request/response validation |
| `requirements.txt` | Python dependencies |
| `Procfile` | Railway deployment config |
| `.env` | Environment variables (NOT in git) |
| `alembic/` | Database migrations |
| `verify_db.py` | Database verification script |

## Key Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload

# Verify database
python verify_db.py

# Create new migration
alembic revision --autogenerate -m "Description"

# Push to GitHub
git add .
git commit -m "Message"
git push origin main
```

## Environment Variables

All in `.env` file (already configured):
- `SUPABASE_URL` - Your Supabase project URL
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - Encryption key (auto-generated)
- `ENVIRONMENT` - `development` (local) or `production` (Railway)

## Database Schema

5 tables created by Alembic migrations:

1. **users** - Customer accounts
2. **locations** - Business locations with NAP data
3. **agent_configs** - Agent settings (6 per location)
4. **oauth_tokens** - OAuth tokens (encrypted)
5. **tasks** - Background job queue

## API Endpoints

- `GET /` - Service info
- `GET /health` - Health check
- `POST /api/onboarding/submit` - Create user + location + agents

## Architecture

```
User fills form → POST /api/onboarding/submit
                     ↓
                  FastAPI validates (Pydantic)
                     ↓
                  Create User record
                     ↓
                  Create Location record
                     ↓
                  Create 6 AgentConfigs (GBP, NAP, Keyword, Blog, Social, Reporting)
                     ↓
                  Save to Supabase Postgres
                     ↓
                  Return user_id + location_id
```

## Success Criteria

✅ Local server starts without errors
✅ Health check returns 200 OK
✅ Onboarding endpoint accepts and saves data
✅ Database shows data in Supabase dashboard
✅ Code pushed to GitHub successfully
✅ Railway deployment succeeds
✅ Production API responds to health check

## Time Estimate

- Local setup: 20 minutes
- GitHub push: 2 minutes
- Railway deployment: 10 minutes
- **Total: ~30 minutes**

## You're Ready!

Once all 3 steps are complete, you have:
- ✅ Production-ready backend API
- ✅ Database with proper schema
- ✅ Automatic deployments from GitHub
- ✅ Foundation to build all 6 agents

**Let's go!** 🚀
