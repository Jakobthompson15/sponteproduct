"""
Pydantic schemas for Agent Outputs.
"""

from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional, Dict, Any, List
from app.models.agent_output import OutputStatus, OutputType, GBPCallToAction


class AgentOutputBase(BaseModel):
    """Base schema for Agent Output."""
    task_id: UUID4
    location_id: UUID4
    output_type: OutputType
    title: Optional[str] = None
    content: str
    call_to_action: Optional[GBPCallToAction] = None
    media_urls: Optional[List[str]] = None
    output_metadata: Optional[Dict[str, Any]] = None


class AgentOutputCreate(AgentOutputBase):
    """Schema for creating an Agent Output."""
    pass


class AgentOutputUpdate(BaseModel):
    """Schema for updating an Agent Output."""
    status: Optional[OutputStatus] = None
    title: Optional[str] = None
    content: Optional[str] = None
    call_to_action: Optional[GBPCallToAction] = None
    media_urls: Optional[List[str]] = None
    platform_post_id: Optional[str] = None
    platform_url: Optional[str] = None
    performance_data: Optional[Dict[str, Any]] = None
    posted_at: Optional[datetime] = None
    scheduled_for: Optional[datetime] = None


class AgentOutputResponse(AgentOutputBase):
    """Schema for Agent Output API response."""
    id: UUID4
    status: OutputStatus
    platform_post_id: Optional[str] = None
    platform_url: Optional[str] = None
    performance_data: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    posted_at: Optional[datetime] = None
    scheduled_for: Optional[datetime] = None

    class Config:
        from_attributes = True  # For Pydantic v2 (was orm_mode in v1)


class AgentOutputListResponse(BaseModel):
    """Schema for list of Agent Outputs."""
    outputs: list[AgentOutputResponse]
    total: int
    page: int
    page_size: int


class GBPPostGenerateRequest(BaseModel):
    """Schema for requesting GBP post generation."""
    location_id: UUID4
    context: Optional[str] = None  # Additional context for content generation


class GBPPostGenerateResponse(BaseModel):
    """Schema for GBP post generation response."""
    task_id: UUID4
    output_id: UUID4
    content: str
    call_to_action: GBPCallToAction
    reasoning: str  # AI's explanation of why this post will work
