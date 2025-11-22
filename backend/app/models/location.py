"""
Location model - represents a business location with NAP (Name, Address, Phone) data.
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.database import Base


class Location(Base):
    """
    Business location table.
    Stores NAP (Name, Address, Phone) data and business details.
    Each user can have multiple locations (for multi-location businesses).
    """
    __tablename__ = "locations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # NAP Data (Name, Address, Phone) - Critical for local SEO
    business_name = Column(String, nullable=False)  # Legal business name
    dba_name = Column(String, nullable=True)  # "Doing Business As" name (optional)
    street_address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    phone_primary = Column(String, nullable=False)
    phone_secondary = Column(String, nullable=True)  # Optional secondary number

    # Business Details
    website_url = Column(String, nullable=True)
    cms_platform = Column(String, nullable=True)  # wordpress, shopify, wix, etc.
    primary_category = Column(String, nullable=False)  # e.g., "Pizza Restaurant", "Dentist"
    services = Column(JSONB, nullable=True)  # Array of services offered

    # Content & Brand Settings (from onboarding)
    brand_tone = Column(String, nullable=True)  # professional, casual, friendly, etc.
    blog_cadence = Column(String, nullable=True)  # weekly, biweekly, monthly
    gbp_cadence = Column(String, nullable=True)  # daily, weekly, biweekly
    forbidden_words = Column(Text, nullable=True)  # Comma-separated list
    forbidden_topics = Column(Text, nullable=True)  # Comma-separated list

    # Goals & Reporting
    primary_goal = Column(String, nullable=True)  # more_calls, more_traffic, more_reviews, etc.
    report_frequency = Column(String, nullable=True)  # weekly, monthly
    report_emails = Column(Text, nullable=True)  # Comma-separated email list

    # Google Business Profile Integration
    gbp_location_name = Column(String, nullable=True)  # Google's location resource name (e.g., 'locations/123456')

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="locations")
    agent_configs = relationship("AgentConfig", back_populates="location", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="location", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="location", cascade="all, delete-orphan")
    agent_tasks = relationship("AgentTask", back_populates="location", cascade="all, delete-orphan")
    agent_outputs = relationship("AgentOutput", back_populates="location", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Location {self.business_name} - {self.city}, {self.state}>"
