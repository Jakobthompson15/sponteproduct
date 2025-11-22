"""
Health check endpoint for monitoring and Railway deployment verification.
"""

from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    Returns 200 OK if the service is running.

    Usage:
    - Railway uses this to verify deployment
    - Monitoring tools can ping this endpoint
    - No authentication required
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Sponte AI Backend"
    }
