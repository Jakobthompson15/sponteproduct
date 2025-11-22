# Sponte AI Backend

Backend API and agent system for Sponte AI - an autonomous local SEO platform powered by AI agents.

## Architecture

- **Framework**: FastAPI (Python 3.13+)
- **Database**: PostgreSQL (Supabase)
- **Task Queue**: Celery + Redis
- **Deployment**: Railway
- **LLM**: Anthropic Claude (content generation)

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Environment configuration
│   ├── database.py          # SQLAlchemy setup
│   ├── models/              # Database models
│   │   ├── user.py          # User accounts
│   │   ├── location.py      # Business locations (NAP data)
│   │   ├── agent_config.py  # Agent configurations
│   │   ├── oauth_token.py   # OAuth tokens (encrypted)
│   │   └── task.py          # Background task queue
│   ├── routers/             # API endpoints
│   │   ├── health.py        # Health check
│   │   └── onboarding.py    # Onboarding form submission
│   ├── schemas/             # Pydantic validation schemas
│   │   └── onboarding.py
│   └── utils/
│       └── encryption.py    # Token encryption utilities
├── alembic/                 # Database migrations
├── requirements.txt         # Python dependencies
├── Procfile                 # Railway deployment config
└── .env                     # Environment variables (not in git)
```

## Database Schema

### Tables

1. **users** - User accounts
   - email, subscription_tier, onboarding_completed

2. **locations** - Business locations
   - NAP data (name, address, phone)
   - Website, CMS platform, category, services
   - Content preferences (brand tone, cadence, forbidden words)
   - Goals and reporting settings

3. **agent_configs** - Agent configurations
   - 6 agents per location (GBP, NAP, Keyword, Blog, Social, Reporting)
   - Autonomy mode (draft, approve, auto)
   - Agent-specific settings (JSON)

4. **oauth_tokens** - OAuth tokens (encrypted)
   - Tokens for Google, Meta, LinkedIn, WordPress, TikTok
   - Access and refresh tokens (encrypted)

5. **tasks** - Background job queue
   - Task type, status, results
   - Scheduled/started/completed timestamps

## Local Development Setup

### Prerequisites

- Python 3.13+
- PostgreSQL (or Supabase account)
- Redis (optional for local dev, required for production)

### Installation

1. **Clone and navigate to backend directory**
```bash
cd /Users/jakobthompson/Desktop/personal/rankingme/backend
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your actual credentials
```

Required environment variables:
- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_ANON_KEY` - Supabase anon public key
- `SUPABASE_SERVICE_KEY` - Supabase service role key
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - Random secret key for encryption
- `REDIS_URL` - Redis connection URL

5. **Run database migrations**
```bash
alembic upgrade head
```

6. **Start the development server**
```bash
uvicorn app.main:app --reload --port 8000
```

Server will start at: `http://localhost:8000`
API docs: `http://localhost:8000/docs`

### Testing

**Health Check**
```bash
curl http://localhost:8000/health
```

**Submit Onboarding (example)**
```bash
curl -X POST http://localhost:8000/api/onboarding/submit \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "businessName": "Test Business LLC",
    "streetAddress": "123 Main St",
    "city": "Chicago",
    "state": "IL",
    "zipCode": "60601",
    "phone": "(312) 555-1234",
    "primaryCategory": "Restaurant"
  }'
```

## Database Migrations

**Create a new migration**
```bash
alembic revision --autogenerate -m "Description of changes"
```

**Apply migrations**
```bash
alembic upgrade head
```

**Rollback migration**
```bash
alembic downgrade -1
```

## Deployment to Railway

### Setup

1. **Sign up for Railway**
   - Go to [railway.app](https://railway.app)
   - Sign in with GitHub

2. **Create new project**
   - New Project → Deploy from GitHub repo
   - Select `Jakobthompson15/spontebackend`
   - Railway auto-detects Python

3. **Add environment variables**
   - Click Variables tab
   - Add all variables from .env file
   - Change `ENVIRONMENT=production`

4. **Add Redis database**
   - Click "New" → "Database" → "Add Redis"
   - Railway automatically adds `REDIS_URL` variable

5. **Deploy**
   - Railway auto-deploys on git push to main
   - Check deployment logs for any errors

6. **Get production URL**
   - Settings → Domains → Generate Domain
   - You'll get: `https://spontebackend-production-xxxx.up.railway.app`

### Verify Deployment

```bash
curl https://spontebackend-production-xxxx.up.railway.app/health
```

Should return:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-15T...",
  "service": "Sponte AI Backend"
}
```

## API Endpoints

### Health Check
`GET /health`
- No authentication required
- Returns service status

### Onboarding
`POST /api/onboarding/submit`
- Submit onboarding form data
- Creates user, location, and agent configs
- Returns user_id and location_id

### API Documentation
`GET /docs` (development only)
- Interactive Swagger UI
- Test endpoints directly in browser

## Next Steps

After Phase 1 is complete, we'll build:

1. **Google OAuth Flow** - Connect GBP, GSC, GA4
2. **GBP Agent** - Sync NAP, create posts, monitor insights
3. **Keyword Agent** - Research keywords with DataForSEO
4. **Blog Agent** - Generate content with Claude, publish to WordPress
5. **Reporting Agent** - Aggregate data, email reports
6. **Dashboard** - Simple UI for users to manage agents

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `SUPABASE_URL` | Supabase project URL | `https://xxx.supabase.co` |
| `SUPABASE_ANON_KEY` | Public anon key | `eyJhb...` |
| `SUPABASE_SERVICE_KEY` | Service role secret | `eyJhb...` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:pass@db...` |
| `SECRET_KEY` | Random secret for encryption | Generate with `python -c "import secrets; print(secrets.token_urlsafe(32))"` |
| `ENVIRONMENT` | Environment mode | `development` or `production` |
| `REDIS_URL` | Redis connection URL | `redis://localhost:6379` |
| `ANTHROPIC_API_KEY` | Claude API key (Phase 2+) | `sk-ant-...` |
| `CORS_ORIGINS` | Allowed frontend domains | `http://localhost:3000,https://...` |

## Support

For issues or questions, contact the development team or create an issue in the GitHub repository.

## License

Proprietary - Sponte AI
