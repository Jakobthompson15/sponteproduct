"""
Agent Output model.
Tracks what AI agents have produced (posts, articles, citations, etc.).
"""

from sqlalchemy import Column, String, Enum, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
from datetime import datetime
import enum


class OutputStatus(str, enum.Enum):
    """Status of agent output."""
    DRAFT = "draft"  # Generated but not approved
    APPROVED = "approved"  # Approved, ready to post
    SCHEDULED = "scheduled"  # Scheduled for future posting
    POSTED = "posted"  # Successfully posted to platform
    FAILED = "failed"  # Failed to post


class OutputType(str, enum.Enum):
    """Type of content output."""
    GBP_POST = "gbp_post"
    BLOG_POST = "blog_post"
    SOCIAL_POST = "social_post"
    CITATION = "citation"
    REVIEW_RESPONSE = "review_response"
    KEYWORD_REPORT = "keyword_report"


class GBPCallToAction(str, enum.Enum):
    """Google Business Profile call-to-action types."""
    BOOK = "BOOK"
    ORDER = "ORDER"
    SHOP = "SHOP"
    LEARN_MORE = "LEARN_MORE"
    SIGN_UP = "SIGN_UP"
    CALL = "CALL"


class AgentOutput(Base):
    """
    Agent Output model.

    Represents content created by AI agents (posts, articles, etc.).
    Each output is linked to a task that generated it.
    """
    __tablename__ = "agent_outputs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("agent_tasks.id"), nullable=False)
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id"), nullable=False)

    output_type = Column(Enum(OutputType), nullable=False)
    status = Column(Enum(OutputStatus), nullable=False, default=OutputStatus.DRAFT)

    # Content fields
    title = Column(String(500), nullable=True)  # For blogs, social posts
    content = Column(Text, nullable=False)  # Main content
    call_to_action = Column(Enum(GBPCallToAction), nullable=True)  # For GBP posts

    # Media
    media_urls = Column(JSONB, nullable=True)  # Array of image/video URLs

    # Platform-specific data
    platform_post_id = Column(String(255), nullable=True)  # ID from external platform (GBP, social, etc.)
    platform_url = Column(String(1000), nullable=True)  # URL to view post on platform

    # Performance tracking
    performance_data = Column(JSONB, nullable=True)  # Views, clicks, engagement, etc.

    # Metadata
    output_metadata = Column(JSONB, nullable=True)  # AI reasoning, prompt used, etc.

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    posted_at = Column(DateTime, nullable=True)  # When actually posted to platform
    scheduled_for = Column(DateTime, nullable=True)  # For scheduled posts

    # Relationships
    task = relationship("AgentTask", back_populates="outputs")
    location = relationship("Location", back_populates="agent_outputs")

    def __repr__(self):
        return f"<AgentOutput {self.id} - {self.output_type} [{self.status}]>"
