"""
AgentConfig model - configuration for each agent type per location.
"""

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from app.database import Base


class AgentType(str, enum.Enum):
    """Available agent types."""
    GBP = "gbp"  # Google Business Profile Agent
    NAP = "nap"  # NAP Consistency Agent
    KEYWORD = "keyword"  # Keyword Research Agent
    BLOG = "blog"  # Blog Content Agent
    SOCIAL = "social"  # Social Media Agent
    REPORTING = "reporting"  # Reporting Agent


class AutonomyMode(str, enum.Enum):
    """Agent autonomy levels."""
    DRAFT = "draft"  # Agent creates drafts, user must manually review and publish
    AUTOPILOT = "autopilot"  # Full autopilot, agent creates and publishes automatically


class AgentConfig(Base):
    """
    Agent configuration table.
    Each location has 6 agent configs (one for each agent type).
    Controls agent behavior and autonomy level.
    """
    __tablename__ = "agent_configs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id", ondelete="CASCADE"), nullable=False, index=True)

    agent_type = Column(Enum(AgentType), nullable=False)
    autonomy_mode = Column(Enum(AutonomyMode), default=AutonomyMode.DRAFT, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    # Agent-specific configuration stored as JSON
    # Examples:
    # - GBP Agent: {"post_frequency": "weekly", "include_utm": true}
    # - Blog Agent: {"min_words": 1500, "include_images": true}
    # - Social Agent: {"platforms": ["facebook", "instagram"], "post_frequency": "daily"}
    config_data = Column(JSONB, nullable=True, default={})

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    location = relationship("Location", back_populates="agent_configs")

    def __repr__(self):
        return f"<AgentConfig {self.agent_type} - {self.autonomy_mode} - Active: {self.is_active}>"
