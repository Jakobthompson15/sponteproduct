"""
Main FastAPI application.
Configures CORS, includes routers, and sets up the API.
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.config import settings
from app.routers import health, onboarding, reports, agents, oauth, locations
from app.database import engine, Base
from app.services.scheduler import start_scheduler, stop_scheduler
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Sponte AI Backend",
    description="Backend API for Sponte AI multi-agent local SEO platform",
    version="1.0.0",
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
)

# Configure CORS (includes localhost:3001)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,  # Frontend domains
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Add validation error handler for debugging
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Log detailed validation errors for debugging"""
    logger.error(f"Validation error for {request.method} {request.url.path}")
    logger.error(f"Validation details: {exc.errors()}")
    logger.error(f"Request body: {await request.body()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )

# Include routers
app.include_router(health.router)
app.include_router(onboarding.router)
app.include_router(reports.router)
app.include_router(agents.router)
app.include_router(oauth.router)
app.include_router(locations.router)


@app.on_event("startup")
async def startup_event():
    """
    Runs when the application starts.
    Test database connection and log startup info.
    """
    logger.info(f"Starting Sponte AI Backend in {settings.ENVIRONMENT} mode")
    logger.info(f"Database: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'N/A'}")

    # Test database connection
    try:
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("✅ Database connection successful")
    except Exception as e:
        logger.error(f"❌ Database connection failed: {str(e)}")
        raise

    # Start the report scheduler
    try:
        start_scheduler()
        logger.info("✅ Report scheduler started successfully")
    except Exception as e:
        logger.error(f"❌ Failed to start report scheduler: {str(e)}")
        # Don't raise - scheduler is not critical for API functionality


@app.on_event("shutdown")
async def shutdown_event():
    """
    Runs when the application shuts down.
    Clean up resources.
    """
    logger.info("Shutting down Sponte AI Backend")

    # Stop the report scheduler
    try:
        stop_scheduler()
        logger.info("✅ Report scheduler stopped successfully")
    except Exception as e:
        logger.error(f"❌ Failed to stop report scheduler: {str(e)}")


@app.get("/")
async def root():
    """
    Root endpoint.
    Returns basic API information.
    """
    return {
        "service": "Sponte AI Backend",
        "version": "1.0.0",
        "status": "running",
        "environment": settings.ENVIRONMENT,
        "docs": "/docs" if settings.ENVIRONMENT == "development" else "disabled in production"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development"
    )
