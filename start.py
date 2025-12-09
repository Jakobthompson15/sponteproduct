#!/usr/bin/env python3
"""Start the FastAPI application with the correct port"""
import os
import uvicorn

if __name__ == "__main__":
    # --- Pre-flight Checks ---
    print("🚀 Starting Sponte AI Backend Startup Script")
    
    # Check Environment
    env = os.environ.get("ENVIRONMENT", "development")
    print(f"ℹ️  Environment: {env}")

    # Check Database URL
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        print("⚠️  WARNING: DATABASE_URL is not set!")
        if env == "production":
            print("❌ FATAL: Cannot run in production without DATABASE_URL.")
            print("   Please check your Railway Variables.")
    else:
        # Mask the password for logging
        try:
            safe_url = db_url.split("@")[1] if "@" in db_url else "..."
            print(f"✅ DATABASE_URL is set (host: {safe_url})")
        except:
            print("✅ DATABASE_URL is set")

    # Check Port
    port_str = os.environ.get("PORT")
    if port_str:
        print(f"✅ PORT is set to {port_str}")
        port = int(port_str)
    else:
        print("ℹ️  PORT is not set. Defaulting to 8000")
        port = 8000

    print(f"🚀 Launching Uvicorn on 0.0.0.0:{port}...")
    print("-" * 50)

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )