"""
Reports API endpoints.
Handles report generation, retrieval, and listing.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.report import (
    ReportResponse,
    ReportListResponse,
    GenerateReportRequest,
)
from app.models import User,  Report, Location, ReportType, AgentTask, AgentOutput
from app.models.agent_task import AgentTaskStatus
from app.models.agent_output import OutputStatus, OutputType
from app.services.email_service import send_report_email
from app.services.google_business_service import GoogleBusinessService
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import func
import logging
import uuid

router = APIRouter(prefix="/api/reports", tags=["Reports"])
logger = logging.getLogger(__name__)


def generate_mock_report_data(location: Location, period_start: datetime, period_end: datetime, db: Optional[Session] = None):
    """
    Generate report data combining real agent activity with mock metrics.
    Real agent data pulled from database when available.
    """
    # Get real agent activity if db session provided
    agent_activity = {}
    if db:
        # GBP Agent Activity
        gbp_tasks_completed = db.query(func.count(AgentTask.id)).filter(
            AgentTask.location_id == location.id,
            AgentTask.agent_type == "GBP",
            AgentTask.status.in_([AgentTaskStatus.COMPLETED, AgentTaskStatus.APPROVED, AgentTaskStatus.POSTED]),
            AgentTask.completed_at >= period_start,
            AgentTask.completed_at <= period_end
        ).scalar() or 0

        gbp_posts_created = db.query(func.count(AgentOutput.id)).filter(
            AgentOutput.location_id == location.id,
            AgentOutput.output_type == OutputType.GBP_POST,
            AgentOutput.created_at >= period_start,
            AgentOutput.created_at <= period_end
        ).scalar() or 0

        gbp_posts_published = db.query(func.count(AgentOutput.id)).filter(
            AgentOutput.location_id == location.id,
            AgentOutput.output_type == OutputType.GBP_POST,
            AgentOutput.status == OutputStatus.POSTED,
            AgentOutput.posted_at >= period_start,
            AgentOutput.posted_at <= period_end
        ).scalar() or 0

        # Blog Agent Activity
        blog_drafts = db.query(func.count(AgentOutput.id)).filter(
            AgentOutput.location_id == location.id,
            AgentOutput.output_type == OutputType.BLOG_POST,
            AgentOutput.status == OutputStatus.DRAFT,
            AgentOutput.created_at >= period_start,
            AgentOutput.created_at <= period_end
        ).scalar() or 0

        blog_published = db.query(func.count(AgentOutput.id)).filter(
            AgentOutput.location_id == location.id,
            AgentOutput.output_type == OutputType.BLOG_POST,
            AgentOutput.status == OutputStatus.POSTED,
            AgentOutput.posted_at >= period_start,
            AgentOutput.posted_at <= period_end
        ).scalar() or 0

        # Build agent activity dict with real data
        agent_activity = {
            "gbp": {
                "postsCreated": gbp_posts_created,
                "postsPublished": gbp_posts_published,
                "tasksCompleted": gbp_tasks_completed
            },
            "nap": {
                "citationsChecked": 0,  # Not implemented yet
                "citationsFixed": 0,
                "tasksCompleted": 0
            },
            "keyword": {
                "keywordsTracked": 0,  # Not implemented yet
                "rankingImprovements": 0,
                "tasksCompleted": 0
            },
            "blog": {
                "draftsCreated": blog_drafts,
                "articlesPublished": blog_published,
                "tasksCompleted": blog_drafts + blog_published
            },
            "social": {
                "postsCreated": 0,  # Not implemented yet
                "postsPublished": 0,
                "tasksCompleted": 0
            },
            "reporting": {
                "reportsGenerated": 1,  # This current report
                "emailsSent": 1,
                "tasksCompleted": 2
            }
        }
    else:
        # Fallback to mock data if no db session
        agent_activity = {
            "gbp": {"postsCreated": 3, "postsPublished": 3, "tasksCompleted": 5},
            "nap": {"citationsChecked": 15, "citationsFixed": 2, "tasksCompleted": 3},
            "keyword": {"keywordsTracked": 25, "rankingImprovements": 7, "tasksCompleted": 4},
            "blog": {"draftsCreated": 2, "articlesPublished": 1, "tasksCompleted": 3},
            "social": {"postsCreated": 4, "postsPublished": 4, "tasksCompleted": 4},
            "reporting": {"reportsGenerated": 1, "emailsSent": 1, "tasksCompleted": 2}
        }

    # Fetch real GBP metrics if location has GBP connected
    metrics_data = {
        "calls": {"current": 127, "previous": 98, "change": 29.6},
        "gbpViews": {"current": 3421, "previous": 2974, "change": 15.2},
        "directionRequests": {"current": 89, "previous": 82, "change": 8.5},
        "websiteClicks": {"current": 234, "previous": 208, "change": 12.5},
        "reviews": {"count": 47, "avgRating": 4.8, "newReviews": 3}
    }

    if db and location.gbp_location_name:
        try:
            # Fetch real GBP insights
            insights = GoogleBusinessService.get_location_insights(
                db=db,
                location_id=str(location.id),
                gbp_location_name=location.gbp_location_name,
                start_date=period_start,
                end_date=period_end
            )

            if insights:
                parsed_insights = GoogleBusinessService.parse_insights_response(insights)

                # Update metrics with real data
                if parsed_insights.get("calls_current") is not None:
                    prev_calls = parsed_insights.get("calls_previous", metrics_data["calls"]["previous"])
                    current_calls = parsed_insights["calls_current"]
                    change = ((current_calls - prev_calls) / prev_calls * 100) if prev_calls > 0 else 0
                    metrics_data["calls"] = {
                        "current": current_calls,
                        "previous": prev_calls,
                        "change": round(change, 1)
                    }

                if parsed_insights.get("views_current") is not None:
                    prev_views = parsed_insights.get("views_previous", metrics_data["gbpViews"]["previous"])
                    current_views = parsed_insights["views_current"]
                    change = ((current_views - prev_views) / prev_views * 100) if prev_views > 0 else 0
                    metrics_data["gbpViews"] = {
                        "current": current_views,
                        "previous": prev_views,
                        "change": round(change, 1)
                    }

                if parsed_insights.get("directions_current") is not None:
                    prev_directions = parsed_insights.get("directions_previous", metrics_data["directionRequests"]["previous"])
                    current_directions = parsed_insights["directions_current"]
                    change = ((current_directions - prev_directions) / prev_directions * 100) if prev_directions > 0 else 0
                    metrics_data["directionRequests"] = {
                        "current": current_directions,
                        "previous": prev_directions,
                        "change": round(change, 1)
                    }

                if parsed_insights.get("website_clicks_current") is not None:
                    prev_clicks = parsed_insights.get("website_clicks_previous", metrics_data["websiteClicks"]["previous"])
                    current_clicks = parsed_insights["website_clicks_current"]
                    change = ((current_clicks - prev_clicks) / prev_clicks * 100) if prev_clicks > 0 else 0
                    metrics_data["websiteClicks"] = {
                        "current": current_clicks,
                        "previous": prev_clicks,
                        "change": round(change, 1)
                    }

                logger.info(f"Successfully fetched real GBP insights for location {location.id}")

        except Exception as e:
            logger.warning(f"Failed to fetch GBP insights: {str(e)}. Using mock data.")

    return {
        "period": f"{period_start.strftime('%b %d, %Y')} to {period_end.strftime('%b %d, %Y')}",
        "metrics": metrics_data,
        "agentActivity": agent_activity,
        "insights": [
            f"Your calls increased 29.6% this period - excellent work!",
            f"GBP profile views are up 15.2%, showing strong local visibility",
            f"Direction requests increased 8.5%, indicating more foot traffic potential",
            f"You've received 3 new reviews, maintaining a stellar 4.8-star rating"
        ],
        "opportunities": [
            "Peak engagement detected Tue-Thu 10am-2pm → Optimizing GBP posting schedule to match audience activity",
            "7 high-performing keywords identified → Creating targeted content pipeline to capitalize on momentum",
            "Strong review engagement rate maintained → Continuing current response strategy (avoiding over-automation)",
            "Social media performance trending up → Monitoring for optimal posting frequency (preventing market saturation)"
        ]
    }


@router.get("/{location_id}", response_model=ReportListResponse)
async def list_reports(
    location_id: str,
    report_type: Optional[ReportType] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),

    db: Session = Depends(get_db)
):
    """
    List all reports for a location, with optional filtering by type.
    Supports pagination.
    """
    try:
        location_uuid = uuid.UUID(location_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid location ID format")

    # Verify location exists
    location = db.query(Location).filter(Location.id == location_uuid).first()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    # Build query
    query = db.query(Report).filter(Report.location_id == location_uuid)

    if report_type:
        query = query.filter(Report.report_type == report_type)

    # Get total count
    total = query.count()

    # Get paginated results
    reports = query.order_by(desc(Report.period_end)).offset((page - 1) * page_size).limit(page_size).all()

    return ReportListResponse(
        reports=[ReportResponse.from_orm(r) for r in reports],
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/{location_id}/latest", response_model=dict)
async def get_latest_reports(
    location_id: str,
    current_user: User = Depends(get_current_user),

    db: Session = Depends(get_db)
):
    """
    Get the latest weekly and monthly reports for a location.
    """
    try:
        location_uuid = uuid.UUID(location_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid location ID format")

    # Get latest weekly report
    latest_weekly = db.query(Report).filter(
        Report.location_id == location_uuid,
        Report.report_type == ReportType.WEEKLY
    ).order_by(desc(Report.period_end)).first()

    # Get latest monthly report
    latest_monthly = db.query(Report).filter(
        Report.location_id == location_uuid,
        Report.report_type == ReportType.MONTHLY
    ).order_by(desc(Report.period_end)).first()

    return {
        "weekly": ReportResponse.from_orm(latest_weekly) if latest_weekly else None,
        "monthly": ReportResponse.from_orm(latest_monthly) if latest_monthly else None
    }


@router.get("/report/{report_id}", response_model=ReportResponse)
async def get_report(
    report_id: str,
    current_user: User = Depends(get_current_user),

    db: Session = Depends(get_db)
):
    """
    Get a specific report by ID.
    """
    try:
        report_uuid = uuid.UUID(report_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid report ID format")

    report = db.query(Report).filter(Report.id == report_uuid).first()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    return ReportResponse.from_orm(report)


@router.post("/generate", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
async def generate_report(
    request: GenerateReportRequest,
    current_user: User = Depends(get_current_user),

    db: Session = Depends(get_db)
):
    """
    Generate a new report for a location.
    Optionally sends email to recipients.
    """
    try:
        location_uuid = uuid.UUID(request.location_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid location ID format")

    # Verify location exists
    location = db.query(Location).filter(Location.id == location_uuid).first()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    # Generate report data with real agent activity
    report_data = generate_mock_report_data(location, request.period_start, request.period_end, db)

    # Create report
    report = Report(
        location_id=location_uuid,
        report_type=request.report_type,
        period_start=request.period_start,
        period_end=request.period_end,
        data=report_data,
        email_recipients=location.report_emails if request.send_email else None,
        email_sent=None  # Will set after successful email send
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    logger.info(f"Generated {request.report_type.value} report for location {request.location_id}")

    # Send email if requested
    if request.send_email and location.report_emails:
        try:
            send_report_email(
                recipient_emails=location.report_emails,
                business_name=location.business_name,
                report_type=request.report_type.value,
                report_data=report_data,
                report_id=str(report.id)
            )
            # Update report to mark email as sent
            report.email_sent = datetime.utcnow()
            db.commit()
            db.refresh(report)
            logger.info(f"Report email sent successfully to {location.report_emails}")
        except Exception as e:
            logger.error(f"Failed to send report email: {str(e)}")
            # Don't fail the request - report was still created

    return ReportResponse.from_orm(report)


@router.post("/test-email")
async def send_test_email(
    current_user: User = Depends(get_current_user),

    db: Session = Depends(get_db)
):
    """
    Send a test report email to jakobnthompson@gmail.com.
    This endpoint is for testing the email template design.
    """
    # Create mock report data
    mock_location = type('obj', (object,), {
        'business_name': 'Demo Pizza Restaurant',
        'report_emails': 'jakobnthompson@gmail.com'
    })()

    period_start = datetime.now() - timedelta(days=7)
    period_end = datetime.now()
    report_data = generate_mock_report_data(mock_location, period_start, period_end)

    # Generate a fake report ID for the link
    mock_report_id = str(uuid.uuid4())

    try:
        send_report_email(
            recipient_emails="jakobnthompson@gmail.com",
            business_name="Demo Pizza Restaurant",
            report_type="weekly",
            report_data=report_data,
            report_id=mock_report_id
        )

        return {
            "success": True,
            "message": "Test email sent to jakobnthompson@gmail.com",
            "note": "Check your inbox to see the email template!"
        }
    except Exception as e:
        logger.error(f"Failed to send test email: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send test email: {str(e)}"
        )
