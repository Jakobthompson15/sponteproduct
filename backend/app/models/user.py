"""
User model - represents a Sponte AI user account.
"""

from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from app.database import Base


class SubscriptionTier(str, enum.Enum):
    """Subscription tier options."""
    STARTER = "starter"
    PRO = "pro"
    AGENCY = "agency"


class User(Base):
    """
    User account table.
    Represents a single Sponte AI customer.
    """
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    clerk_user_id = Column(String, unique=True, nullable=False, index=True)  # Clerk's user ID
    email = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    onboarding_completed = Column(Boolean, default=False, nullable=False)
    subscription_tier = Column(
        Enum(SubscriptionTier),
        default=SubscriptionTier.STARTER,
        nullable=False
    )

    # Relationships
    locations = relationship("Location", back_populates="user", cascade="all, delete-orphan")
    oauth_tokens = relationship("OAuthToken", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.email} ({self.subscription_tier})>"
