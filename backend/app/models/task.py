"""
Task model - represents background jobs executed by Celery workers (agents).
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from app.database import Base


class TaskStatus(str, enum.Enum):
    """Task execution status."""
    PENDING = "pending"  # Task scheduled but not started
    RUNNING = "running"  # Task currently executing
    COMPLETED = "completed"  # Task finished successfully
    FAILED = "failed"  # Task encountered an error


class TaskType(str, enum.Enum):
    """Types of tasks agents can perform."""
    # GBP Agent tasks
    SYNC_NAP = "sync_nap"  # Sync NAP data to GBP
    CREATE_GBP_POST = "create_gbp_post"  # Create and publish GBP post
    FETCH_GBP_INSIGHTS = "fetch_gbp_insights"  # Get performance data

    # NAP Agent tasks
    VERIFY_NAP = "verify_nap"  # Check NAP consistency across platforms
    GENERATE_NAP_REPORT = "generate_nap_report"  # Create NAP audit report

    # Keyword Agent tasks
    RESEARCH_KEYWORDS = "research_keywords"  # Fetch keyword data from DataForSEO
    ANALYZE_RANKINGS = "analyze_rankings"  # Check current rankings

    # Blog Agent tasks
    GENERATE_BLOG = "generate_blog"  # Write blog post with Claude
    PUBLISH_BLOG = "publish_blog"  # Publish to WordPress/CMS

    # Social Agent tasks
    CREATE_SOCIAL_POST = "create_social_post"  # Generate social media content
    PUBLISH_SOCIAL = "publish_social"  # Post to social platforms

    # Reporting Agent tasks
    GENERATE_REPORT = "generate_report"  # Create weekly/monthly report
    SEND_REPORT = "send_report"  # Email report to user


class Task(Base):
    """
    Background task queue table.
    Tracks all agent operations and their status.
    """
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id", ondelete="CASCADE"), nullable=False, index=True)

    agent_type = Column(String, nullable=False)  # gbp, nap, keyword, blog, social, reporting
    task_type = Column(Enum(TaskType), nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False, index=True)

    # Scheduling
    scheduled_at = Column(DateTime(timezone=True), nullable=False)  # When task should run
    started_at = Column(DateTime(timezone=True), nullable=True)  # When task actually started
    completed_at = Column(DateTime(timezone=True), nullable=True)  # When task finished

    # Results and errors
    error_message = Column(Text, nullable=True)  # Error details if task failed
    result_data = Column(JSONB, nullable=True)  # Task output/results as JSON

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    location = relationship("Location", back_populates="tasks")

    def __repr__(self):
        return f"<Task {self.task_type} - {self.status}>"
