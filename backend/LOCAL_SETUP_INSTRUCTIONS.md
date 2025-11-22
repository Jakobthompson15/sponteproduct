# Local Setup Instructions

Follow these steps to set up and test the backend locally before deploying to Railway.

## Step 1: Create Virtual Environment and Install Dependencies

```bash
cd /Users/jakobthompson/Desktop/personal/rankingme/backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

You should see a bunch of packages being installed (FastAPI, SQLAlchemy, Alembic, etc.)

## Step 2: Run Database Migrations

This creates all the tables in your Supabase database.

```bash
# Still in the backend directory with venv activated
alembic upgrade head
```

You should see output like:
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> xxxx, Initial schema
```

## Step 3: Verify Database Setup

```bash
python verify_db.py
```

You should see:
```
============================================================
SPONTE AI - DATABASE VERIFICATION
============================================================

✅ Database connection successful

📊 Tables found: 5
   - agent_configs
   - locations
   - oauth_tokens
   - tasks
   - users

📈 Data Summary:
   Users:        0
   Locations:    0
   Agent Configs: 0
   OAuth Tokens: 0
   Tasks:        0

============================================================
✅ Database verification complete!
============================================================
```

## Step 4: Start the Development Server

```bash
uvicorn app.main:app --reload --port 8000
```

You should see:
```
INFO:     Will watch for changes in these directories: ['/Users/jakobthompson/Desktop/personal/rankingme/backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using StatReload
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Starting Sponte AI Backend in development mode
INFO:     Database: db.mtksypjvfrdskrlvunsv.supabase.co:5432/postgres
INFO:     ✅ Database connection successful
INFO:     Application startup complete.
```

## Step 5: Test the API

Open a **new terminal window** (keep the server running) and test:

### Test Health Endpoint

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-15T...",
  "service": "Sponte AI Backend"
}
```

### Test Root Endpoint

```bash
curl http://localhost:8000/
```

Expected response:
```json
{
  "service": "Sponte AI Backend",
  "version": "1.0.0",
  "status": "running",
  "environment": "development",
  "docs": "/docs"
}
```

### View API Documentation

Open in browser:
```
http://localhost:8000/docs
```

You'll see interactive Swagger UI with all endpoints!

### Test Onboarding Endpoint

```bash
curl -X POST http://localhost:8000/api/onboarding/submit \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "businessName": "Test Pizzeria LLC",
    "dbaName": "Test Pizza",
    "streetAddress": "123 Main Street",
    "city": "Chicago",
    "state": "IL",
    "zipCode": "60601",
    "phone": "(312) 555-1234",
    "primaryCategory": "Pizza Restaurant",
    "websiteUrl": "https://testpizza.com",
    "cmsPlatform": "wordpress",
    "services": "Dine-in\nTakeout\nDelivery",
    "brandTone": "friendly",
    "blogCadence": "weekly",
    "gbpCadence": "weekly",
    "globalAutonomy": "draft",
    "primaryGoal": "more_calls",
    "reportFrequency": "weekly",
    "reportEmails": "test@example.com"
  }'
```

Expected response:
```json
{
  "success": true,
  "message": "Onboarding completed successfully! Check your email for next steps.",
  "user_id": "550e8400-...",
  "location_id": "660e8400-...",
  "next_steps": [
    "Check your email for a welcome message",
    "Connect your Google Business Profile",
    "Connect your Google Search Console",
    "Connect your WordPress site (if applicable)",
    "Review your agent settings in the dashboard"
  ]
}
```

## Step 6: Verify Data Was Saved

```bash
python verify_db.py
```

Now you should see:
```
📈 Data Summary:
   Users:        1
   Locations:    1
   Agent Configs: 6
   OAuth Tokens: 0
   Tasks:        0

👥 USERS (1):
   - test@example.com
     ID: 550e8400-...
     Tier: starter
     Onboarding: ✅ Complete
     Locations: 1

📍 LOCATIONS (1):
   - Test Pizzeria LLC
     DBA: Test Pizza
     Address: 123 Main Street, Chicago, IL 60601
     Phone: (312) 555-1234
     Category: Pizza Restaurant
     Website: https://testpizza.com
     CMS: wordpress
     Agents: 6

🤖 AGENT CONFIGURATIONS (6):
   - blog: 1 configured
   - gbp: 1 configured
   - keyword: 1 configured
   - nap: 1 configured
   - reporting: 1 configured
   - social: 1 configured
```

## Step 7: Check Supabase Dashboard

1. Go to [supabase.com](https://supabase.com)
2. Open your `sponte-ai` project
3. Go to **Table Editor**
4. You should see all 5 tables with data!

Click on each table:
- `users` - 1 row with your test user
- `locations` - 1 row with the business data
- `agent_configs` - 6 rows (one for each agent)
- `oauth_tokens` - 0 rows (we'll add these in Phase 2)
- `tasks` - 0 rows (will be populated when agents run)

## ✅ Success!

If all tests pass, your backend is working perfectly locally!

## Next Steps

1. **Push code to GitHub** (see GIT_PUSH_INSTRUCTIONS.md)
2. **Deploy to Railway** (I'll guide you through this)
3. **Update frontend** to connect to Railway API
4. **Test end-to-end** flow

## Troubleshooting

### Database Connection Error

If you see: `psycopg2.OperationalError: could not connect to server`

- Check your `.env` file has correct `DATABASE_URL`
- Verify Supabase project is running (not paused)
- Check your internet connection

### Import Errors

If you see: `ModuleNotFoundError: No module named 'fastapi'`

- Make sure you activated the virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### Alembic Migration Error

If migrations fail:

```bash
# Delete alembic/versions folder and regenerate
rm -rf alembic/versions/*.py
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```

## Stop the Server

When you're done testing, press `CTRL+C` in the terminal where uvicorn is running.

To deactivate the virtual environment:
```bash
deactivate
```
