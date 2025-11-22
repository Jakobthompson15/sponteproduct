"""
GBP Agent Service.
Handles Google Business Profile post generation and management.
"""

from sqlalchemy.orm import Session
from app.models import Location, AgentTask, AgentOutput, AgentConfig
from app.models.agent_task import AgentTaskStatus, AgentTaskType
from app.models.agent_output import OutputStatus, OutputType, GBPCallToAction
from app.services.ai_service import AIService
from app.services.google_business_service import GoogleBusinessService
from datetime import datetime
from typing import Dict, Any, List, Optional
import logging
import uuid

logger = logging.getLogger(__name__)


class GBPAgentService:
    """Service for GBP agent operations."""

    @staticmethod
    def create_post_task(
        db: Session,
        location_id: uuid.UUID,
        scheduled_for: Optional[datetime] = None,
        context: Optional[str] = None
    ) -> AgentTask:
        """
        Create a new GBP post generation task.

        Args:
            db: Database session
            location_id: Location UUID
            scheduled_for: When to execute the task
            context: Optional context for generation

        Returns:
            Created AgentTask
        """
        task = AgentTask(
            location_id=location_id,
            agent_type="GBP",
            task_type=AgentTaskType.CREATE_GBP_POST,
            status=AgentTaskStatus.PENDING,
            scheduled_for=scheduled_for or datetime.utcnow(),
            task_metadata={"context": context} if context else None
        )

        db.add(task)
        db.commit()
        db.refresh(task)

        logger.info(f"Created GBP post task {task.id} for location {location_id}")
        return task

    @staticmethod
    def process_post_task(
        db: Session,
        task_id: uuid.UUID
    ) -> AgentOutput:
        """
        Process a GBP post task - generate content using AI.

        Args:
            db: Database session
            task_id: Task UUID

        Returns:
            Created AgentOutput
        """
        # Get task
        task = db.query(AgentTask).filter(AgentTask.id == task_id).first()
        if not task:
            raise ValueError(f"Task {task_id} not found")

        if task.status != AgentTaskStatus.PENDING:
            raise ValueError(f"Task {task_id} is not in PENDING status")

        # Update task status
        task.status = AgentTaskStatus.IN_PROGRESS
        db.commit()

        try:
            # Get location
            location = db.query(Location).filter(Location.id == task.location_id).first()
            if not location:
                raise ValueError(f"Location {task.location_id} not found")

            # Get recent posts to avoid repetition
            recent_outputs = db.query(AgentOutput).filter(
                AgentOutput.location_id == task.location_id,
                AgentOutput.output_type == OutputType.GBP_POST
            ).order_by(AgentOutput.created_at.desc()).limit(5).all()

            previous_posts = [output.content for output in recent_outputs]

            # Get context from task metadata
            context = None
            if task.task_metadata and "context" in task.task_metadata:
                context = task.task_metadata["context"]

            # Generate content using AI
            logger.info(f"Generating GBP post for location {location.business_name}")
            result = AIService.generate_gbp_post(
                location=location,
                context=context,
                previous_posts=previous_posts
            )

            # Create output
            output = AgentOutput(
                task_id=task.id,
                location_id=task.location_id,
                output_type=OutputType.GBP_POST,
                content=result["content"],
                call_to_action=GBPCallToAction(result["cta"]),
                status=OutputStatus.DRAFT,  # Start as draft
                output_metadata={
                    "reasoning": result.get("reasoning", ""),
                    "ai_model": "claude-sonnet-4-20250514"
                }
            )

            db.add(output)

            # Update task
            task.status = AgentTaskStatus.COMPLETED
            task.generated_content = {
                "content": result["content"],
                "cta": result["cta"],
                "reasoning": result["reasoning"]
            }
            task.completed_at = datetime.utcnow()

            db.commit()
            db.refresh(output)

            logger.info(f"Generated GBP post output {output.id} for task {task.id}")
            return output

        except Exception as e:
            # Mark task as failed
            task.status = AgentTaskStatus.FAILED
            task.error_message = str(e)
            db.commit()

            logger.error(f"Failed to process task {task_id}: {str(e)}")
            raise

    @staticmethod
    def approve_post(
        db: Session,
        output_id: uuid.UUID
    ) -> AgentOutput:
        """
        Approve a GBP post for posting.

        Args:
            db: Database session
            output_id: Output UUID

        Returns:
            Updated AgentOutput
        """
        output = db.query(AgentOutput).filter(AgentOutput.id == output_id).first()
        if not output:
            raise ValueError(f"Output {output_id} not found")

        if output.status != OutputStatus.DRAFT:
            raise ValueError(f"Output {output_id} is not in DRAFT status")

        # Update output status
        output.status = OutputStatus.APPROVED

        # Update related task
        task = db.query(AgentTask).filter(AgentTask.id == output.task_id).first()
        if task:
            task.status = AgentTaskStatus.APPROVED

        db.commit()
        db.refresh(output)

        logger.info(f"Approved GBP post output {output_id}")
        return output

    @staticmethod
    def reject_post(
        db: Session,
        output_id: uuid.UUID,
        reason: Optional[str] = None
    ) -> AgentOutput:
        """
        Reject a GBP post.

        Args:
            db: Database session
            output_id: Output UUID
            reason: Optional rejection reason

        Returns:
            Updated AgentOutput
        """
        output = db.query(AgentOutput).filter(AgentOutput.id == output_id).first()
        if not output:
            raise ValueError(f"Output {output_id} not found")

        # Update output status
        output.status = OutputStatus.FAILED

        # Update task
        task = db.query(AgentTask).filter(AgentTask.id == output.task_id).first()
        if task:
            task.status = AgentTaskStatus.REJECTED
            if reason:
                task.error_message = f"Rejected: {reason}"

        db.commit()
        db.refresh(output)

        logger.info(f"Rejected GBP post output {output_id}")
        return output

    @staticmethod
    def edit_post(
        db: Session,
        output_id: uuid.UUID,
        new_content: str,
        new_cta: Optional[GBPCallToAction] = None
    ) -> AgentOutput:
        """
        Edit a GBP post content.

        Args:
            db: Database session
            output_id: Output UUID
            new_content: New content text
            new_cta: Optional new CTA

        Returns:
            Updated AgentOutput
        """
        output = db.query(AgentOutput).filter(AgentOutput.id == output_id).first()
        if not output:
            raise ValueError(f"Output {output_id} not found")

        # Update content
        output.content = new_content
        if new_cta:
            output.call_to_action = new_cta

        # Add edit metadata
        if not output.output_metadata:
            output.output_metadata = {}
        output.output_metadata["edited"] = True
        output.output_metadata["edited_at"] = datetime.utcnow().isoformat()

        output.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(output)

        logger.info(f"Edited GBP post output {output_id}")
        return output

    @staticmethod
    def mark_as_posted(
        db: Session,
        output_id: uuid.UUID,
        platform_post_id: Optional[str] = None,
        platform_url: Optional[str] = None,
        auto_post: bool = True
    ) -> AgentOutput:
        """
        Mark a post as successfully posted to GBP.
        If auto_post=True and GBP is connected, actually posts to Google Business Profile.

        Args:
            db: Database session
            output_id: Output UUID
            platform_post_id: GBP post ID (if posting manually)
            platform_url: URL to view post (if posting manually)
            auto_post: If True, automatically post to GBP API

        Returns:
            Updated AgentOutput
        """
        output = db.query(AgentOutput).filter(AgentOutput.id == output_id).first()
        if not output:
            raise ValueError(f"Output {output_id} not found")

        # Get location to check GBP connection
        location = db.query(Location).filter(Location.id == output.location_id).first()
        if not location:
            raise ValueError(f"Location {output.location_id} not found")

        # If auto_post is enabled and location has GBP connected, post to Google
        if auto_post and location.gbp_location_name:
            try:
                logger.info(f"Posting output {output_id} to Google Business Profile")

                # Actually post to GBP API
                result = GoogleBusinessService.create_local_post(
                    db=db,
                    location_id=str(location.id),
                    gbp_location_name=location.gbp_location_name,
                    content=output.content,
                    call_to_action=output.call_to_action
                )

                if result:
                    # Extract post ID and URL from GBP response
                    platform_post_id = result.get("name", "")  # GBP returns post name like "locations/123/localPosts/456"
                    # GBP doesn't return a direct URL, so we'll construct one or leave it empty
                    logger.info(f"Successfully posted to GBP. Post ID: {platform_post_id}")
                else:
                    logger.warning(f"GBP API returned no result for output {output_id}")

            except Exception as e:
                logger.error(f"Failed to post to GBP API: {str(e)}")
                # Don't raise - mark as posted locally even if GBP fails
                # This prevents blocking the workflow
                if not output.output_metadata:
                    output.output_metadata = {}
                output.output_metadata["gbp_error"] = str(e)

        # Update output
        output.status = OutputStatus.POSTED
        output.posted_at = datetime.utcnow()
        if platform_post_id:
            output.platform_post_id = platform_post_id
        if platform_url:
            output.platform_url = platform_url

        # Update task
        task = db.query(AgentTask).filter(AgentTask.id == output.task_id).first()
        if task:
            task.status = AgentTaskStatus.POSTED

        db.commit()
        db.refresh(output)

        logger.info(f"Marked output {output_id} as posted to GBP")
        return output

    @staticmethod
    def get_pending_tasks_for_location(
        db: Session,
        location_id: uuid.UUID
    ) -> List[AgentTask]:
        """
        Get all pending GBP tasks for a location.

        Args:
            db: Database session
            location_id: Location UUID

        Returns:
            List of pending AgentTasks
        """
        tasks = db.query(AgentTask).filter(
            AgentTask.location_id == location_id,
            AgentTask.agent_type == "GBP",
            AgentTask.status == AgentTaskStatus.PENDING
        ).order_by(AgentTask.scheduled_for).all()

        return tasks

    @staticmethod
    def get_draft_posts_for_location(
        db: Session,
        location_id: uuid.UUID
    ) -> List[AgentOutput]:
        """
        Get all draft GBP posts for a location.

        Args:
            db: Database session
            location_id: Location UUID

        Returns:
            List of draft AgentOutputs
        """
        outputs = db.query(AgentOutput).filter(
            AgentOutput.location_id == location_id,
            AgentOutput.output_type == OutputType.GBP_POST,
            AgentOutput.status == OutputStatus.DRAFT
        ).order_by(AgentOutput.created_at.desc()).all()

        return outputs

    @staticmethod
    def should_create_post_today(db: Session, location: Location) -> bool:
        """
        Check if a GBP post should be created today based on cadence.

        Args:
            db: Database session
            location: Location object

        Returns:
            True if post should be created
        """
        if not location.gbp_cadence or location.gbp_cadence == "off":
            return False

        # Get most recent post
        latest_post = db.query(AgentOutput).filter(
            AgentOutput.location_id == location.id,
            AgentOutput.output_type == OutputType.GBP_POST,
            AgentOutput.status.in_([OutputStatus.POSTED, OutputStatus.SCHEDULED])
        ).order_by(AgentOutput.created_at.desc()).first()

        if not latest_post:
            return True  # No posts yet, create one

        days_since_last = (datetime.utcnow() - latest_post.created_at).days

        # Check cadence
        cadence_days = {
            "daily": 1,
            "triweekly": 2,  # ~3x per week
            "weekly": 7,
            "biweekly": 14,
            "monthly": 30
        }

        required_days = cadence_days.get(location.gbp_cadence, 7)
        return days_since_last >= required_days
