"""
OAuthToken model - stores encrypted OAuth tokens for third-party integrations.
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from app.database import Base


class OAuthProvider(str, enum.Enum):
    """OAuth providers we integrate with."""
    GOOGLE = "google"  # For GBP, GSC, GA4
    META = "meta"  # For Facebook/Instagram
    LINKEDIN = "linkedin"  # For LinkedIn company pages
    WORDPRESS = "wordpress"  # WordPress sites (may use API key instead)
    TIKTOK = "tiktok"  # TikTok Business


class OAuthToken(Base):
    """
    OAuth token storage table.
    Stores encrypted access and refresh tokens for third-party API access.
    Users grant permission once, tokens stored securely.
    """
    __tablename__ = "oauth_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id", ondelete="CASCADE"), nullable=True, index=True)  # Optional: tokens can be per-location

    provider = Column(Enum(OAuthProvider), nullable=False)

    # Encrypted tokens (use encryption.py utilities to encrypt/decrypt)
    access_token_encrypted = Column(Text, nullable=False)
    refresh_token_encrypted = Column(Text, nullable=True)  # Some providers don't give refresh tokens

    # Token metadata
    expires_at = Column(DateTime(timezone=True), nullable=True)  # When access token expires
    scope = Column(Text, nullable=True)  # OAuth scopes granted (e.g., "profile email https://www.googleapis.com/auth/business.manage")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="oauth_tokens")

    def __repr__(self):
        return f"<OAuthToken {self.provider} for user {self.user_id}>"
