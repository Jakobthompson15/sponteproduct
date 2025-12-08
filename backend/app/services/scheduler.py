"""
Scheduled jobs for automated report generation.
Handles weekly (every Monday) and monthly (first Monday) report generation.
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Location, Report, ReportType, AgentConfig
from app.models.agent_config import AutonomyMode
from app.routers.reports import generate_mock_report_data
from app.services.email_service import send_report_email
from app.services.gbp_agent import GBPAgentService
import logging

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()


def get_db_session():
    """Create a database session for scheduled jobs."""
    db = SessionLocal()
    try:
        return db
    finally:
        pass  # Don't close here, caller will close


def is_first_monday_of_month() -> bool:
    """Check if today is the first Monday of the month."""
    today = datetime.now()
    if today.weekday() != 0:  # Not Monday
        return False

    # Check if this is the first Monday (day 1-7)
    return 1 <= today.day <= 7


def generate_weekly_reports():
    """
    Generate weekly reports for all locations.
    Runs every Monday at 8:00 AM.
    """
    logger.info("Starting weekly report generation job...")
    db = SessionLocal()

    try:
        # Get all locations with report_emails configured
        locations = db.query(Location).filter(
            Location.report_emails.isnot(None),
            Location.report_emails != ""
        ).all()

        logger.info(f"Found {len(locations)} locations with email reporting enabled")

        # Calculate date range (previous Monday to Sunday)
        today = datetime.now()
        days_since_monday = today.weekday()
        last_monday = today - timedelta(days=days_since_monday + 7)
        last_sunday = last_monday + timedelta(days=6)

        # Set to start/end of day
        period_start = last_monday.replace(hour=0, minute=0, second=0, microsecond=0)
        period_end = last_sunday.replace(hour=23, minute=59, second=59, microsecond=999999)

        success_count = 0
        error_count = 0

        for location in locations:
            try:
                # Generate report data
                report_data = generate_mock_report_data(location, period_start, period_end, db)

                # Create report in database
                report = Report(
                    location_id=location.id,
                    report_type=ReportType.WEEKLY,
                    period_start=period_start,
                    period_end=period_end,
                    data=report_data,
                    email_recipients=location.report_emails,
                    email_sent=None
                )

                db.add(report)
                db.commit()
                db.refresh(report)

                logger.info(f"Created weekly report for location {location.business_name} ({location.id})")

                # Send email
                try:
                    send_report_email(
                        recipient_emails=location.report_emails,
                        business_name=location.business_name,
                        report_type='weekly',
                        report_data=report_data,
                        report_id=str(report.id)
                    )

                    # Update email_sent timestamp
                    report.email_sent = datetime.utcnow()
                    db.commit()

                    logger.info(f"Sent weekly report email to {location.report_emails}")
                    success_count += 1

                except Exception as e:
                    logger.error(f"Failed to send weekly report email for {location.business_name}: {str(e)}")
                    error_count += 1
                    # Report is still created, just email failed

            except Exception as e:
                logger.error(f"Failed to generate weekly report for {location.business_name}: {str(e)}")
                error_count += 1
                db.rollback()

        logger.info(f"Weekly report job completed. Success: {success_count}, Errors: {error_count}")

    except Exception as e:
        logger.error(f"Weekly report job failed: {str(e)}")

    finally:
        db.close()


def generate_monthly_reports():
    """
    Generate monthly reports for all locations.
    Runs on the first Monday of each month at 9:00 AM.
    """
    logger.info("Starting monthly report generation job...")

    # Double-check we're on first Monday
    if not is_first_monday_of_month():
        logger.info("Not the first Monday of the month, skipping monthly reports")
        return

    db = SessionLocal()

    try:
        # Get all locations with report_emails configured
        locations = db.query(Location).filter(
            Location.report_emails.isnot(None),
            Location.report_emails != ""
        ).all()

        logger.info(f"Found {len(locations)} locations for monthly reporting")

        # Calculate date range (previous month)
        today = datetime.now()
        first_of_this_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_month_end = first_of_this_month - timedelta(days=1)
        last_month_start = last_month_end.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        period_start = last_month_start
        period_end = last_month_end.replace(hour=23, minute=59, second=59, microsecond=999999)

        success_count = 0
        error_count = 0

        for location in locations:
            try:
                # Generate report data
                report_data = generate_mock_report_data(location, period_start, period_end, db)

                # Create report in database
                report = Report(
                    location_id=location.id,
                    report_type=ReportType.MONTHLY,
                    period_start=period_start,
                    period_end=period_end,
                    data=report_data,
                    email_recipients=location.report_emails,
                    email_sent=None
                )

                db.add(report)
                db.commit()
                db.refresh(report)

                logger.info(f"Created monthly report for location {location.business_name} ({location.id})")

                # Send email
                try:
                    send_report_email(
                        recipient_emails=location.report_emails,
                        business_name=location.business_name,
                        report_type='monthly',
                        report_data=report_data,
                        report_id=str(report.id)
                    )

                    # Update email_sent timestamp
                    report.email_sent = datetime.utcnow()
                    db.commit()

                    logger.info(f"Sent monthly report email to {location.report_emails}")
                    success_count += 1

                except Exception as e:
                    logger.error(f"Failed to send monthly report email for {location.business_name}: {str(e)}")
                    error_count += 1

            except Exception as e:
                logger.error(f"Failed to generate monthly report for {location.business_name}: {str(e)}")
                error_count += 1
                db.rollback()

        logger.info(f"Monthly report job completed. Success: {success_count}, Errors: {error_count}")

    except Exception as e:
        logger.error(f"Monthly report job failed: {str(e)}")

    finally:
        db.close()


def create_gbp_tasks():
    """
    Create GBP post tasks for locations based on their cadence.
    Runs daily at 6:00 AM.
    If location is in AUTOPILOT mode, immediately processes and posts the content.
    """
    logger.info("Starting GBP task creation job...")
    db = SessionLocal()

    try:
        # Get all locations with GBP cadence configured
        locations = db.query(Location).filter(
            Location.gbp_cadence.isnot(None),
            Location.gbp_cadence != "off"
        ).all()

        logger.info(f"Found {len(locations)} locations with GBP posting enabled")

        tasks_created = 0
        posts_auto_generated = 0
        errors = 0

        for location in locations:
            try:
                # Check if post should be created today
                should_create = GBPAgentService.should_create_post_today(db, location)

                if not should_create:
                    logger.debug(f"Skipping {location.business_name} - not due for post yet")
                    continue

                # Get agent config for this location
                gbp_config = db.query(AgentConfig).filter(
                    AgentConfig.location_id == location.id,
                    AgentConfig.agent_type == "GBP"
                ).first()

                if not gbp_config or not gbp_config.is_active:
                    logger.info(f"Skipping {location.business_name} - GBP agent not active")
                    continue

                # Create task
                task = GBPAgentService.create_post_task(
                    db=db,
                    location_id=location.id,
                    context=f"Scheduled {location.gbp_cadence} post"
                )
                tasks_created += 1
                logger.info(f"Created GBP task for {location.business_name}")

                # If AUTOPILOT mode, process immediately
                if gbp_config.autonomy_mode == AutonomyMode.AUTOPILOT:
                    try:
                        # Process task (generate content)
                        output = GBPAgentService.process_post_task(db, task.id)

                        # Auto-approve
                        output = GBPAgentService.approve_post(db, output.id)

                        # Post to Google Business Profile
                        output = GBPAgentService.mark_as_posted(db, output.id)

                        posts_auto_generated += 1
                        logger.info(f"AUTOPILOT: Auto-generated and posted content for {location.business_name}")

                    except Exception as e:
                        logger.error(f"Failed to auto-process task for {location.business_name}: {str(e)}")
                        errors += 1

                else:
                    logger.info(f"DRAFT MODE: Task created for {location.business_name}, awaiting human approval")

            except Exception as e:
                logger.error(f"Failed to create GBP task for {location.business_name}: {str(e)}")
                errors += 1

        logger.info(f"GBP task creation job completed. Tasks: {tasks_created}, Auto-posted: {posts_auto_generated}, Errors: {errors}")

    except Exception as e:
        logger.error(f"GBP task creation job failed: {str(e)}")

    finally:
        db.close()


def start_scheduler():
    """
    Start the scheduler with all scheduled jobs.
    Called when the FastAPI application starts.
    """
    logger.info("Starting report scheduler...")

    # Weekly reports: Every Monday at 8:00 AM
    scheduler.add_job(
        generate_weekly_reports,
        trigger=CronTrigger(day_of_week='mon', hour=8, minute=0),
        id='weekly_reports',
        name='Generate Weekly Reports',
        replace_existing=True
    )
    logger.info("Scheduled weekly reports job: Every Monday at 8:00 AM")

    # Monthly reports: Every Monday at 9:00 AM (will check if it's first Monday)
    scheduler.add_job(
        generate_monthly_reports,
        trigger=CronTrigger(day_of_week='mon', hour=9, minute=0),
        id='monthly_reports',
        name='Generate Monthly Reports',
        replace_existing=True
    )
    logger.info("Scheduled monthly reports job: First Monday of each month at 9:00 AM")

    # GBP task creation: Every day at 6:00 AM
    scheduler.add_job(
        create_gbp_tasks,
        trigger=CronTrigger(hour=6, minute=0),
        id='gbp_task_creation',
        name='Create GBP Tasks',
        replace_existing=True
    )
    logger.info("Scheduled GBP task creation job: Every day at 6:00 AM")

    scheduler.start()
    logger.info("Report scheduler started successfully")


def stop_scheduler():
    """
    Stop the scheduler gracefully.
    Called when the FastAPI application shuts down.
    """
    logger.info("Stopping report scheduler...")
    scheduler.shutdown()
    logger.info("Report scheduler stopped")
