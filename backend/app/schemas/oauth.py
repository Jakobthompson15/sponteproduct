"""
Pydantic schemas for OAuth-related API requests and responses.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ConnectionStatus(BaseModel):
    """Status of a single OAuth connection."""
    provider: str
    connected: bool
    connected_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    needs_reconnection: bool = False


class ConnectionsStatusResponse(BaseModel):
    """Response with all OAuth connection statuses for a location."""
    location_id: str
    google_business_profile: ConnectionStatus
    google_search_console: ConnectionStatus
    google_analytics: ConnectionStatus
    wordpress: ConnectionStatus
    meta: ConnectionStatus
    linkedin: ConnectionStatus

    class Config:
        json_schema_extra = {
            "example": {
                "location_id": "550e8400-e29b-41d4-a716-446655440000",
                "google_business_profile": {
                    "provider": "google",
                    "connected": True,
                    "connected_at": "2025-11-20T12:00:00Z",
                    "expires_at": "2025-12-20T12:00:00Z",
                    "needs_reconnection": False
                },
                "google_search_console": {
                    "provider": "google",
                    "connected": False,
                    "needs_reconnection": False
                },
                "google_analytics": {
                    "provider": "google",
                    "connected": False,
                    "needs_reconnection": False
                },
                "wordpress": {
                    "provider": "wordpress",
                    "connected": False,
                    "needs_reconnection": False
                },
                "meta": {
                    "provider": "meta",
                    "connected": False,
                    "needs_reconnection": False
                },
                "linkedin": {
                    "provider": "linkedin",
                    "connected": False,
                    "needs_reconnection": False
                }
            }
        }
