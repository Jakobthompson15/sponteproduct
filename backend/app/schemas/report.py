"""
Pydantic schemas for report API requests and responses.
"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.report import ReportType


class ReportMetric(BaseModel):
    """Individual metric with current value and change"""
    current: int | float
    previous: int | float
    change: float  # Percentage change


class ReportMetrics(BaseModel):
    """Collection of all metrics in a report"""
    calls: Optional[ReportMetric] = None
    gbp_views: Optional[ReportMetric] = None
    direction_requests: Optional[ReportMetric] = None
    website_clicks: Optional[ReportMetric] = None
    reviews_count: Optional[int] = None
    avg_rating: Optional[float] = None


class AgentActivity(BaseModel):
    """Activity stats for a single agent"""
    posts_created: Optional[int] = 0
    posts_published: Optional[int] = 0
    tasks_completed: Optional[int] = 0
    items_pending: Optional[int] = 0


class ReportData(BaseModel):
    """Full report data structure"""
    metrics: ReportMetrics
    agent_activity: Optional[Dict[str, AgentActivity]] = {}
    insights: Optional[List[str]] = []
    recommendations: Optional[List[str]] = []


class ReportResponse(BaseModel):
    """Response for a single report"""
    id: str
    location_id: str
    report_type: ReportType
    period_start: datetime
    period_end: datetime
    data: Dict[str, Any]  # Stored as JSONB
    email_sent: Optional[datetime] = None
    email_recipients: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=str(obj.id),
            location_id=str(obj.location_id),
            report_type=obj.report_type,
            period_start=obj.period_start,
            period_end=obj.period_end,
            data=obj.data,
            email_sent=obj.email_sent,
            email_recipients=obj.email_recipients,
            created_at=obj.created_at
        )


class ReportListResponse(BaseModel):
    """Response for list of reports"""
    reports: List[ReportResponse]
    total: int
    page: int
    page_size: int


class GenerateReportRequest(BaseModel):
    """Request to generate a new report"""
    location_id: str
    report_type: ReportType
    period_start: datetime
    period_end: datetime
    send_email: bool = False
