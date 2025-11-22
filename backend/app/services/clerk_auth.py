"""
Clerk Authentication Service.
Handles JWT token verification and user authentication with Clerk.
"""

import jwt
import requests
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models import User
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class ClerkAuth:
    """Service for Clerk authentication operations."""

    _jwks_cache: Optional[Dict[str, Any]] = None

    @classmethod
    def clear_cache(cls):
        """Clear the JWKS cache (useful for testing or key rotation)."""
        cls._jwks_cache = None

    @staticmethod
    def get_jwks() -> Dict[str, Any]:
        """
        Fetch Clerk's JSON Web Key Set (JWKS) for JWT verification.
        Cached to avoid repeated network calls.
        """
        if ClerkAuth._jwks_cache:
            return ClerkAuth._jwks_cache

        try:
            # Extract frontend API from the publishable key
            # Format: pk_test_<base64_encoded_frontend_api>
            import base64

            key = settings.CLERK_PUBLISHABLE_KEY
            if key.startswith('pk_test_'):
                encoded_part = key.replace('pk_test_', '')
            elif key.startswith('pk_live_'):
                encoded_part = key.replace('pk_live_', '')
            else:
                raise ValueError("Invalid Clerk publishable key format")

            # Decode base64 to get frontend API URL
            # Add padding if needed
            padding = len(encoded_part) % 4
            if padding:
                encoded_part += '=' * (4 - padding)

            clerk_frontend_api = base64.b64decode(encoded_part).decode('utf-8').rstrip('$')
            jwks_url = f"https://{clerk_frontend_api}/.well-known/jwks.json"

            logger.info(f"Fetching JWKS from: {jwks_url}")
            response = requests.get(jwks_url, timeout=10)
            response.raise_for_status()

            ClerkAuth._jwks_cache = response.json()
            return ClerkAuth._jwks_cache

        except Exception as e:
            logger.error(f"Failed to fetch Clerk JWKS: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Authentication service unavailable"
            )

    @staticmethod
    def verify_token(token: str) -> Dict[str, Any]:
        """
        Verify a Clerk JWT token and return the claims.

        Args:
            token: JWT token from Clerk

        Returns:
            Dict with token claims (including 'sub' which is the Clerk user ID)

        Raises:
            HTTPException if token is invalid
        """
        try:
            # Get JWKS
            jwks = ClerkAuth.get_jwks()

            # Decode token header to get the key ID
            unverified_header = jwt.get_unverified_header(token)
            key_id = unverified_header.get('kid')

            if not key_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token: missing key ID"
                )

            # Find the public key matching the key ID
            public_key = None
            for key in jwks['keys']:
                if key['kid'] == key_id:
                    public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)
                    break

            if not public_key:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token: public key not found"
                )

            # Verify and decode the token
            # Allow 60 seconds leeway for clock skew
            claims = jwt.decode(
                token,
                public_key,
                algorithms=['RS256'],
                options={
                    "verify_signature": True,
                    "verify_exp": True,
                    "verify_iat": True,
                },
                leeway=60  # Allow 60 seconds clock skew
            )

            return claims

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.InvalidTokenError as e:
            logger.error(f"Invalid JWT token: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        except Exception as e:
            logger.error(f"Token verification error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token verification failed"
            )

    @staticmethod
    def get_or_create_user(db: Session, clerk_user_id: str, email: str) -> User:
        """
        Get existing user or create new user from Clerk authentication.

        Args:
            db: Database session
            clerk_user_id: Clerk's user ID
            email: User email from Clerk

        Returns:
            User object
        """
        # Try to find user by Clerk user ID
        user = db.query(User).filter(User.clerk_user_id == clerk_user_id).first()

        if user:
            # Update email if it changed
            if user.email != email:
                user.email = email
                db.commit()
                db.refresh(user)
            return user

        # Check if user exists with this email but different Clerk ID (migration case)
        user = db.query(User).filter(User.email == email).first()

        if user:
            # Update the Clerk user ID for legacy users
            user.clerk_user_id = clerk_user_id
            db.commit()
            db.refresh(user)
            logger.info(f"Updated legacy user {email} with Clerk user ID")
            return user

        # Create new user
        user = User(
            clerk_user_id=clerk_user_id,
            email=email,
            onboarding_completed=False
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        logger.info(f"Created new user from Clerk: {email}")
        return user
