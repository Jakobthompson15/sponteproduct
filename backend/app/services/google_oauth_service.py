"""
Google OAuth Service.
Handles OAuth 2.0 authentication flow for Google My Business API.
"""

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from app.config import settings
from app.models import OAuthToken, Location
from app.models.oauth_token import OAuthProvider
from app.utils.encryption import encrypt_token, decrypt_token
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, List
import logging
import json
import uuid

logger = logging.getLogger(__name__)

# Google My Business API scopes
SCOPES = [
    'https://www.googleapis.com/auth/business.manage',  # Manage business listings
    'https://www.googleapis.com/auth/userinfo.email',   # Get user email
    'https://www.googleapis.com/auth/userinfo.profile', # Get user profile
    'openid'                                             # OpenID Connect (automatically added by Google)
]


class GoogleOAuthService:
    """Service for Google OAuth operations."""

    @staticmethod
    def create_oauth_flow() -> Flow:
        """
        Create a Google OAuth flow.

        Returns:
            Flow object for OAuth

        Raises:
            ValueError if Google OAuth not configured
        """
        if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
            raise ValueError("Google OAuth credentials not configured. Please set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in .env file.")

        client_config = {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uris": [settings.GOOGLE_REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        }

        flow = Flow.from_client_config(
            client_config=client_config,
            scopes=SCOPES,
            redirect_uri=settings.GOOGLE_REDIRECT_URI
        )

        return flow

    @staticmethod
    def get_authorization_url(state: str) -> str:
        """
        Get the Google OAuth authorization URL.

        Args:
            state: State parameter for CSRF protection

        Returns:
            Authorization URL
        """
        flow = GoogleOAuthService.create_oauth_flow()
        authorization_url, _ = flow.authorization_url(
            access_type='offline',  # Request refresh token
            include_granted_scopes='true',
            state=state,
            prompt='consent'  # Force consent screen to get refresh token
        )

        logger.info(f"Generated authorization URL with state: {state}")
        return authorization_url

    @staticmethod
    def exchange_code_for_tokens(code: str) -> Dict[str, Any]:
        """
        Exchange authorization code for access and refresh tokens.

        Args:
            code: Authorization code from Google

        Returns:
            Dict with token information
        """
        import requests

        # Exchange code for tokens using direct HTTP request
        # This bypasses the scope validation issue in google-auth-oauthlib
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            'code': code,
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'redirect_uri': settings.GOOGLE_REDIRECT_URI,
            'grant_type': 'authorization_code'
        }

        response = requests.post(token_url, data=data)
        response.raise_for_status()
        token_data = response.json()

        # Calculate expiry time
        expires_in = token_data.get('expires_in', 3600)
        expiry = datetime.now(timezone.utc) + timedelta(seconds=expires_in)

        return {
            "access_token": token_data['access_token'],
            "refresh_token": token_data.get('refresh_token'),
            "token_uri": "https://oauth2.googleapis.com/token",
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "scopes": token_data.get('scope', '').split(' '),
            "expiry": expiry
        }

    @staticmethod
    def save_tokens(
        db: Session,
        location_id: str,
        token_data: Dict[str, Any],
        provider_user_id: Optional[str] = None
    ) -> OAuthToken:
        """
        Save OAuth tokens to database.

        Args:
            db: Database session
            location_id: Location UUID
            token_data: Token data from Google
            provider_user_id: Google user ID (email)

        Returns:
            Created OAuthToken
        """
        # Get the location to retrieve user_id
        location_uuid = uuid.UUID(location_id) if isinstance(location_id, str) else location_id
        location = db.query(Location).filter(Location.id == location_uuid).first()
        if not location:
            raise ValueError(f"Location {location_id} not found")

        # Encrypt tokens
        access_token_encrypted = encrypt_token(token_data["access_token"])
        refresh_token_encrypted = encrypt_token(token_data.get("refresh_token")) if token_data.get("refresh_token") else None

        # Check if token already exists for this location
        existing_token = db.query(OAuthToken).filter(
            OAuthToken.location_id == location_uuid,
            OAuthToken.provider == OAuthProvider.GOOGLE
        ).first()

        if existing_token:
            # Update existing token
            existing_token.access_token_encrypted = access_token_encrypted
            if refresh_token_encrypted:
                existing_token.refresh_token_encrypted = refresh_token_encrypted
            existing_token.expires_at = token_data.get("expiry")
            existing_token.scope = ' '.join(token_data.get("scopes", []))
            existing_token.updated_at = datetime.now(timezone.utc)

            db.commit()
            db.refresh(existing_token)

            logger.info(f"Updated Google OAuth token for location {location_id}")
            return existing_token

        # Create new token
        oauth_token = OAuthToken(
            user_id=location.user_id,
            location_id=location_uuid,
            provider=OAuthProvider.GOOGLE,
            access_token_encrypted=access_token_encrypted,
            refresh_token_encrypted=refresh_token_encrypted,
            expires_at=token_data.get("expiry"),
            scope=' '.join(token_data.get("scopes", []))
        )

        db.add(oauth_token)
        db.commit()
        db.refresh(oauth_token)

        logger.info(f"Saved Google OAuth token for location {location_id}")
        return oauth_token

    @staticmethod
    def get_valid_credentials(db: Session, location_id: str) -> Optional[Credentials]:
        """
        Get valid Google credentials for a location.
        Automatically refreshes if expired.

        Args:
            db: Database session
            location_id: Location UUID

        Returns:
            Google Credentials object or None
        """
        oauth_token = db.query(OAuthToken).filter(
            OAuthToken.location_id == location_id,
            OAuthToken.provider == OAuthProvider.GOOGLE
        ).first()

        if not oauth_token:
            logger.warning(f"No Google OAuth token found for location {location_id}")
            return None

        # Decrypt tokens
        access_token = decrypt_token(oauth_token.access_token_encrypted)
        refresh_token = decrypt_token(oauth_token.refresh_token_encrypted) if oauth_token.refresh_token_encrypted else None

        # Parse scopes
        scopes = oauth_token.scope.split(' ') if oauth_token.scope else SCOPES

        # Convert expiry to timezone-naive for Google's credentials library
        # Google's _helpers.utcnow() returns timezone-naive datetime, so we need to match that
        expiry = oauth_token.expires_at
        if expiry and expiry.tzinfo is not None:
            # Convert timezone-aware to timezone-naive UTC
            expiry = expiry.replace(tzinfo=None)

        # Create credentials object
        credentials = Credentials(
            token=access_token,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            scopes=scopes,
            expiry=expiry
        )

        # Check if expired
        if credentials.expired and credentials.refresh_token:
            try:
                from google.auth.transport.requests import Request
                credentials.refresh(Request())

                # Update token in database with encrypted new token
                oauth_token.access_token_encrypted = encrypt_token(credentials.token)
                oauth_token.expires_at = credentials.expiry
                oauth_token.updated_at = datetime.now(timezone.utc)
                db.commit()

                logger.info(f"Refreshed Google OAuth token for location {location_id}")

            except Exception as e:
                logger.error(f"Failed to refresh Google OAuth token: {str(e)}")
                return None

        return credentials

    @staticmethod
    def disconnect(db: Session, location_id: str) -> bool:
        """
        Disconnect Google OAuth for a location.

        Args:
            db: Database session
            location_id: Location UUID

        Returns:
            True if disconnected, False if not found
        """
        oauth_token = db.query(OAuthToken).filter(
            OAuthToken.location_id == location_id,
            OAuthToken.provider == OAuthProvider.GOOGLE
        ).first()

        if not oauth_token:
            return False

        db.delete(oauth_token)
        db.commit()

        logger.info(f"Disconnected Google OAuth for location {location_id}")
        return True

    @staticmethod
    def get_user_email(credentials: Credentials) -> Optional[str]:
        """
        Get user email from Google OAuth.

        Args:
            credentials: Google Credentials

        Returns:
            User email or None
        """
        try:
            service = build('oauth2', 'v2', credentials=credentials)
            user_info = service.userinfo().get().execute()
            return user_info.get('email')
        except Exception as e:
            logger.error(f"Failed to get user email: {str(e)}")
            return None

    @staticmethod
    def list_accounts(credentials: Credentials) -> List[Dict[str, Any]]:
        """
        List Google My Business accounts.

        Args:
            credentials: Google Credentials

        Returns:
            List of account dicts
        """
        try:
            service = build('mybusinessaccountmanagement', 'v1', credentials=credentials)
            accounts = service.accounts().list().execute()
            return accounts.get('accounts', [])
        except Exception as e:
            logger.error(f"Failed to list Google My Business accounts: {str(e)}")
            return []

    @staticmethod
    def list_locations(credentials: Credentials, account_name: str) -> List[Dict[str, Any]]:
        """
        List locations for a Google My Business account.

        Args:
            credentials: Google Credentials
            account_name: Account resource name (e.g., 'accounts/123')

        Returns:
            List of location dicts
        """
        try:
            service = build('mybusinessbusinessinformation', 'v1', credentials=credentials)
            locations = service.locations().list(parent=account_name).execute()
            return locations.get('locations', [])
        except Exception as e:
            logger.error(f"Failed to list locations for account {account_name}: {str(e)}")
            return []
