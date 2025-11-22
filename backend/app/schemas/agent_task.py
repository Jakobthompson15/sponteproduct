"""
Pydantic schemas for Agent Tasks.
"""

from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional, Dict, Any
from app.models.agent_task import AgentTaskStatus, AgentTaskType


class AgentTaskBase(BaseModel):
    """Base schema for Agent Task."""
    location_id: UUID4
    agent_type: str
    task_type: AgentTaskType
    scheduled_for: Optional[datetime] = None
    task_metadata: Optional[Dict[str, Any]] = None


class AgentTaskCreate(AgentTaskBase):
    """Schema for creating an Agent Task."""
    pass


class AgentTaskUpdate(BaseModel):
    """Schema for updating an Agent Task."""
    status: Optional[AgentTaskStatus] = None
    generated_content: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    completed_at: Optional[datetime] = None


class AgentTaskResponse(AgentTaskBase):
    """Schema for Agent Task API response."""
    id: UUID4
    status: AgentTaskStatus
    generated_content: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # For Pydantic v2 (was orm_mode in v1)


class AgentTaskListResponse(BaseModel):
    """Schema for list of Agent Tasks."""
    tasks: list[AgentTaskResponse]
    total: int
    page: int
    page_size: int
