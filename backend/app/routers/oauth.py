"""
OAuth API endpoints.
Handles OAuth authentication flows for third-party services.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.services.google_oauth_service import GoogleOAuthService
from app.models import Location, User, OAuthToken, OAuthProvider
from app.schemas.oauth import ConnectionsStatusResponse, ConnectionStatus
from typing import Optional
from datetime import datetime, timezone
import logging
import uuid
import secrets

router = APIRouter(prefix="/api/oauth", tags=["OAuth"])
logger = logging.getLogger(__name__)

# Simple file-based state storage (survives backend restarts)
import json
import os
from pathlib import Path

STATE_FILE = Path("/tmp/oauth_states.json")

def load_oauth_states():
    """Load OAuth states from file"""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_oauth_states(states):
    """Save OAuth states to file"""
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(states, f)
    except Exception as e:
        logger.error(f"Failed to save OAuth states: {e}")

# Load existing states on startup
oauth_states = load_oauth_states()


@router.get("/google/connect")
async def connect_google(
    location_id: str,
    db: Session = Depends(get_db)
):
    """
    Initiate Google OAuth flow for a location.
    No authentication required - OAuth with Google provides security.
    CSRF protection via state parameter.

    Args:
        location_id: Location UUID

    Returns:
        Redirect to Google OAuth consent screen
    """
    try:
        location_uuid = uuid.UUID(location_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid location ID format")

    # Verify location exists
    location = db.query(Location).filter(Location.id == location_uuid).first()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    try:
        # Generate random state for CSRF protection
        state = secrets.token_urlsafe(32)

        # Store state with location_id (in production, use Redis with expiry)
        oauth_states[state] = str(location_uuid)
        save_oauth_states(oauth_states)

        # Get authorization URL
        authorization_url = GoogleOAuthService.get_authorization_url(state)

        # Redirect to Google OAuth
        return RedirectResponse(url=authorization_url)

    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Error initiating Google OAuth: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to initiate OAuth: {str(e)}")


@router.get("/google/callback")
async def google_callback(
    code: str = Query(...),
    state: str = Query(...),
    error: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Handle Google OAuth callback.

    Args:
        code: Authorization code from Google
        state: State parameter for CSRF protection
        error: Optional error from Google

    Returns:
        Redirect to frontend with success/error
    """
    # Check for errors
    if error:
        logger.error(f"Google OAuth error: {error}")
        return RedirectResponse(
            url=f"http://localhost:3000/dashboard/settings?oauth_error={error}",
            status_code=status.HTTP_302_FOUND
        )

    # Verify state
    if state not in oauth_states:
        logger.error(f"Invalid OAuth state: {state}")
        raise HTTPException(status_code=400, detail="Invalid state parameter")

    location_id = oauth_states.pop(state)
    save_oauth_states(oauth_states)

    try:
        # Exchange code for tokens
        token_data = GoogleOAuthService.exchange_code_for_tokens(code)

        # Get user email
        from google.oauth2.credentials import Credentials
        credentials = Credentials(
            token=token_data["access_token"],
            refresh_token=token_data.get("refresh_token"),
            token_uri=token_data["token_uri"],
            client_id=token_data["client_id"],
            client_secret=token_data["client_secret"]
        )

        user_email = GoogleOAuthService.get_user_email(credentials)

        # Save tokens to database
        GoogleOAuthService.save_tokens(
            db=db,
            location_id=location_id,
            token_data=token_data,
            provider_user_id=user_email
        )

        logger.info(f"Successfully connected Google account for location {location_id}")

        # Redirect to frontend OAuth callback page
        return RedirectResponse(
            url=f"http://localhost:3001/oauth/google/callback?oauth_success=google&location_id={location_id}",
            status_code=status.HTTP_302_FOUND
        )

    except Exception as e:
        logger.error(f"Error in Google OAuth callback: {str(e)}")
        return RedirectResponse(
            url=f"http://localhost:3001/oauth/google/callback?oauth_error=callback_failed",
            status_code=status.HTTP_302_FOUND
        )


@router.post("/google/disconnect/{location_id}")
async def disconnect_google(
    location_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Disconnect Google OAuth for a location.

    Args:
        location_id: Location UUID

    Returns:
        Success message
    """
    try:
        location_uuid = uuid.UUID(location_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid location ID format")

    # Verify location exists
    location = db.query(Location).filter(Location.id == location_uuid).first()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    success = GoogleOAuthService.disconnect(db, str(location_uuid))

    if not success:
        raise HTTPException(status_code=404, detail="No Google connection found for this location")

    return {"message": "Successfully disconnected Google account"}


@router.get("/google/status/{location_id}")
async def get_google_status(
    location_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Check if Google OAuth is connected for a location.

    Args:
        location_id: Location UUID

    Returns:
        Connection status
    """
    try:
        location_uuid = uuid.UUID(location_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid location ID format")

    # Try to get valid credentials
    credentials = GoogleOAuthService.get_valid_credentials(db, str(location_uuid))

    connected = credentials is not None

    response = {
        "connected": connected,
        "location_id": location_id
    }

    if connected:
        # Get user email
        user_email = GoogleOAuthService.get_user_email(credentials)
        if user_email:
            response["email"] = user_email

        # Get accounts and locations
        accounts = GoogleOAuthService.list_accounts(credentials)
        response["accounts_count"] = len(accounts)

    return response


@router.get("/google/accounts/{location_id}")
async def list_google_accounts(
    location_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List Google My Business accounts for a connected location.

    Args:
        location_id: Location UUID

    Returns:
        List of accounts and their locations
    """
    try:
        location_uuid = uuid.UUID(location_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid location ID format")

    # Get valid credentials
    credentials = GoogleOAuthService.get_valid_credentials(db, str(location_uuid))
    if not credentials:
        raise HTTPException(status_code=404, detail="Google not connected for this location")

    # Get accounts
    accounts = GoogleOAuthService.list_accounts(credentials)

    # Get locations for each account
    accounts_with_locations = []
    for account in accounts:
        account_name = account.get('name')
        locations = GoogleOAuthService.list_locations(credentials, account_name)

        accounts_with_locations.append({
            "account_name": account.get('accountName'),
            "account_number": account.get('accountNumber'),
            "resource_name": account_name,
            "locations": [
                {
                    "name": loc.get('name'),
                    "title": loc.get('title'),
                    "resource_name": loc.get('name'),
                    "address": loc.get('address', {}).get('formattedAddress')
                }
                for loc in locations
            ]
        })

    return {
        "accounts": accounts_with_locations,
        "total_accounts": len(accounts_with_locations)
    }


@router.get("/connections/status", response_model=ConnectionsStatusResponse)
async def get_connections_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get status of all OAuth connections for the current user's location.

    Returns:
        Connection status for all integrations
    """
    # Get user's location
    location = db.query(Location).filter(Location.user_id == current_user.id).first()
    if not location:
        raise HTTPException(status_code=404, detail="No location found for user")

    # Get all OAuth tokens for this location
    oauth_tokens = db.query(OAuthToken).filter(
        OAuthToken.location_id == location.id
    ).all()

    # Build connection status for each provider
    token_map = {token.provider: token for token in oauth_tokens}

    def get_status(provider: OAuthProvider, provider_name: str) -> ConnectionStatus:
        token = token_map.get(provider)
        if not token:
            return ConnectionStatus(
                provider=provider_name,
                connected=False,
                needs_reconnection=False
            )

        # Check if token is expired
        needs_reconnection = False
        if token.expires_at:
            now = datetime.now(timezone.utc)
            if token.expires_at < now:
                needs_reconnection = True

        return ConnectionStatus(
            provider=provider_name,
            connected=True,
            connected_at=token.created_at,
            expires_at=token.expires_at,
            needs_reconnection=needs_reconnection
        )

    # Return status for all integrations
    # Note: Currently we only support Google OAuth, so GSC and GA4 share the same Google connection
    google_token = token_map.get(OAuthProvider.GOOGLE)
    google_status = get_status(OAuthProvider.GOOGLE, "google")

    return ConnectionsStatusResponse(
        location_id=str(location.id),
        google_business_profile=google_status,
        google_search_console=google_status,  # Uses same Google OAuth
        google_analytics=google_status,  # Uses same Google OAuth
        wordpress=ConnectionStatus(provider="wordpress", connected=False, needs_reconnection=False),
        meta=ConnectionStatus(provider="meta", connected=False, needs_reconnection=False),
        linkedin=ConnectionStatus(provider="linkedin", connected=False, needs_reconnection=False)
    )
