# Railway Deployment Troubleshooting Guide

If your application isn't loading on Railway, follow these steps to diagnose and fix the issue.

## 1. Check the Deployment Logs

1. Go to your [Railway Dashboard](https://railway.app/dashboard).
2. Click on the **Sponte Product** project.
3. Click on the **backend** service.
4. Click on the **Deployments** tab.
5. Click on the latest deployment (even if it says "Crashed").
6. Click on **Deploy Logs**.

Look for lines that start with `Error:` or `Traceback`.

## 2. Common Issues

### "Database connection failed" or "KeyError: 'DATABASE_URL'"

The backend strictly requires a database connection to start. If the `DATABASE_URL` environment variable is missing or incorrect, the app will crash immediately.

**Solution:**
1. Navigate to the **Variables** tab in your Railway backend service.
2. Ensure `DATABASE_URL` is set.
3. If you are using a Railway-managed PostgreSQL, it should be auto-populated. If not, use the "Reference Variable" feature to link it to `PostgreSQL.DATABASE_URL`.
   - Value should look like: `${{PostgreSQL.DATABASE_URL}}`

### "Port not bound" or App listening on wrong port

Railway expects the app to listen on the port defined by the `$PORT` environment variable (or port 8000/3000 by default if using their detection).

**Solution:**
We use `start.py` to handle this automatically:
```python
port = int(os.environ.get("PORT", 8000))
# ...
host="0.0.0.0"
```
Ensure you haven't hardcoded `port=8000` or `host="127.0.0.1"` anywhere else if you modified the startup logic.

## 3. Verify Environment Variables

Check `backend/railway-env-vars.txt` for the list of required variables.

**Critical Variables:**
- `DATABASE_URL`
- `ENVIRONMENT` (should be `production`)
- `SECRET_KEY`

## 4. Local Simulation

You can simulate the production startup locally by running:

```bash
# From the root directory
export PORT=8000
export ENVIRONMENT=production
# deliberate missing DATABASE_URL to test crash
python start.py
```

This will run the same script Railway uses.
