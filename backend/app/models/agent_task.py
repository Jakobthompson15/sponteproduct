"""
Agent Task model.
Tracks what each AI agent needs to do (pending work queue).
"""

from sqlalchemy import Column, String, Enum, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
from datetime import datetime
import enum


class AgentTaskStatus(str, enum.Enum):
    """Status of an agent task."""
    PENDING = "pending"  # Task created, waiting to be processed
    IN_PROGRESS = "in_progress"  # AI is generating content
    COMPLETED = "completed"  # Content generated and saved
    APPROVED = "approved"  # User approved (for draft mode)
    REJECTED = "rejected"  # User rejected (for draft mode)
    POSTED = "posted"  # Successfully posted to platform
    FAILED = "failed"  # Task failed with error


class AgentTaskType(str, enum.Enum):
    """Type of task an agent can perform."""
    # GBP Agent
    CREATE_GBP_POST = "create_gbp_post"
    RESPOND_TO_REVIEW = "respond_to_review"
    UPDATE_BUSINESS_HOURS = "update_business_hours"

    # Blog Agent
    CREATE_BLOG_POST = "create_blog_post"
    UPDATE_BLOG_POST = "update_blog_post"

    # Social Agent
    CREATE_SOCIAL_POST = "create_social_post"

    # NAP Agent
    CREATE_CITATION = "create_citation"
    UPDATE_CITATION = "update_citation"

    # Keyword Agent
    RESEARCH_KEYWORDS = "research_keywords"
    TRACK_RANKINGS = "track_rankings"


class AgentTask(Base):
    """
    Agent Task model.

    Represents a single task that an AI agent needs to complete.
    Tasks are created by the scheduler or manually by users.
    """
    __tablename__ = "agent_tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id"), nullable=False)
    agent_type = Column(String(50), nullable=False)  # GBP, BLOG, SOCIAL, etc.
    task_type = Column(Enum(AgentTaskType), nullable=False)
    status = Column(Enum(AgentTaskStatus), nullable=False, default=AgentTaskStatus.PENDING)

    # Scheduling
    scheduled_for = Column(DateTime, nullable=True)  # When task should be executed

    # Content
    generated_content = Column(JSONB, nullable=True)  # AI-generated content (JSON)

    # Metadata
    task_metadata = Column(JSONB, nullable=True)  # Additional context (prompts, settings, etc.)

    # Error handling
    error_message = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    location = relationship("Location", back_populates="agent_tasks")
    outputs = relationship("AgentOutput", back_populates="task")

    def __repr__(self):
        return f"<AgentTask {self.id} - {self.agent_type}:{self.task_type} [{self.status}]>"
