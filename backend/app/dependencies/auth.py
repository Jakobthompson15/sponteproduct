"""
Authentication dependencies for FastAPI routes.
"""

from typing import Optional
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.clerk_auth import ClerkAuth
from app.models import User


async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get the current authenticated user from Clerk JWT token.

    Args:
        authorization: Bearer token from Authorization header
        db: Database session

    Returns:
        Authenticated User object

    Raises:
        HTTPException if authentication fails
    """
    import logging
    logger = logging.getLogger(__name__)

    if not authorization:
        logger.error("Missing authorization header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract token from "Bearer <token>"
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        logger.error(f"Invalid authorization header format: {authorization[:50]}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format. Expected 'Bearer <token>'",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = parts[1]
    logger.info(f"Verifying token: {token[:20]}...")

    # Verify token with Clerk
    try:
        claims = ClerkAuth.verify_token(token)
        logger.info(f"Token verified successfully. Claims: {claims.keys()}")
    except Exception as e:
        logger.error(f"Token verification failed: {str(e)}")
        raise

    # Get Clerk user ID from claims
    clerk_user_id = claims.get("sub")

    if not clerk_user_id:
        logger.error(f"Invalid token claims. Missing sub (user ID)")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token claims"
        )

    # Get email from claims (may not be present in all Clerk configurations)
    email = claims.get("email")

    # If email is not in token, try to get it from existing user in database
    if not email:
        logger.info(f"Email not in token claims, checking database for user {clerk_user_id}")
        user = db.query(User).filter(User.clerk_user_id == clerk_user_id).first()

        if user:
            logger.info(f"Found existing user: {user.email}")
            return user
        else:
            # For new users without email in token, use a placeholder
            # They'll need to update it later or we'll get it from Clerk API
            logger.warning(f"New user {clerk_user_id} has no email in token, using placeholder")
            email = f"{clerk_user_id}@placeholder.local"

    # Get or create user in database
    user = ClerkAuth.get_or_create_user(db, clerk_user_id, email)
    logger.info(f"User authenticated: {user.email}")

    return user


async def get_optional_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Dependency to optionally get the current authenticated user.
    Returns None if no valid authentication is provided.

    Args:
        authorization: Bearer token from Authorization header
        db: Database session

    Returns:
        User object if authenticated, None otherwise
    """
    if not authorization:
        return None

    try:
        return await get_current_user(authorization, db)
    except HTTPException:
        return None
