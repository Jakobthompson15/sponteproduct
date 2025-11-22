"""
Report model for storing generated weekly and monthly reports.
"""

from sqlalchemy import Column, String, DateTime, Enum as SQLEnum, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
from datetime import datetime
import enum


class ReportType(str, enum.Enum):
    """Report frequency types"""
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    CUSTOM = "custom"


class Report(Base):
    """
    Stores generated reports for a location.
    Enables historical report viewing and email delivery tracking.
    """
    __tablename__ = "reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id"), nullable=False)
    report_type = Column(SQLEnum(ReportType), nullable=False)

    # Time period covered by this report
    period_start = Column(DateTime(timezone=True), nullable=False)
    period_end = Column(DateTime(timezone=True), nullable=False)

    # Report data stored as JSON
    # Contains: metrics, agent_activity, insights, recommendations
    data = Column(JSONB, nullable=False, default=dict)

    # Email delivery tracking
    email_sent = Column(DateTime(timezone=True), nullable=True)
    email_recipients = Column(Text, nullable=True)  # Comma-separated list

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    # Relationships
    location = relationship("Location", back_populates="reports")

    def __repr__(self):
        return f"<Report {self.report_type.value} {self.period_start} to {self.period_end}>"
