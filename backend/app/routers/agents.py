"""
Agents API endpoints.
Handles AI agent operations (GBP, Blog, Social, etc.).
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models import AgentTask, AgentOutput, Location, User
from app.schemas.agent_task import (
    AgentTaskResponse,
    AgentTaskListResponse,
    AgentTaskUpdate
)
from app.schemas.agent_output import (
    AgentOutputResponse,
    AgentOutputListResponse,
    AgentOutputUpdate,
    GBPPostGenerateRequest,
    GBPPostGenerateResponse
)
from app.models.agent_output import GBPCallToAction
from app.services.gbp_agent import GBPAgentService
from typing import Optional
import logging
import uuid

router = APIRouter(prefix="/api/agents", tags=["Agents"])
logger = logging.getLogger(__name__)


@router.post("/gbp/generate", response_model=GBPPostGenerateResponse, status_code=status.HTTP_201_CREATED)
async def generate_gbp_post(
    request: GBPPostGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate a new GBP post for a location.
    Creates a task and immediately processes it to generate content.
    Requires Clerk authentication.
    """
    try:
        location_uuid = request.location_id
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid location ID format")

    # Verify location exists
    location = db.query(Location).filter(Location.id == location_uuid).first()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    try:
        # Create task
        task = GBPAgentService.create_post_task(
            db=db,
            location_id=location_uuid,
            context=request.context
        )

        # Process task immediately to generate content
        output = GBPAgentService.process_post_task(
            db=db,
            task_id=task.id
        )

        # Extract reasoning from metadata
        reasoning = ""
        if output.output_metadata and "reasoning" in output.output_metadata:
            reasoning = output.output_metadata["reasoning"]

        return GBPPostGenerateResponse(
            task_id=task.id,
            output_id=output.id,
            content=output.content,
            call_to_action=output.call_to_action,
            reasoning=reasoning
        )

    except Exception as e:
        logger.error(f"Error generating GBP post: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate GBP post: {str(e)}")


@router.get("/gbp/drafts/{location_id}", response_model=AgentOutputListResponse)
async def get_draft_gbp_posts(
    location_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all draft GBP posts for a location.
    """
    try:
        location_uuid = uuid.UUID(location_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid location ID format")

    # Verify location exists
    location = db.query(Location).filter(Location.id == location_uuid).first()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    # Get draft posts
    all_drafts = GBPAgentService.get_draft_posts_for_location(db, location_uuid)
    total = len(all_drafts)

    # Paginate
    start = (page - 1) * page_size
    end = start + page_size
    drafts = all_drafts[start:end]

    return AgentOutputListResponse(
        outputs=[AgentOutputResponse.from_orm(draft) for draft in drafts],
        total=total,
        page=page,
        page_size=page_size
    )


@router.patch("/outputs/{output_id}/approve", response_model=AgentOutputResponse)
async def approve_post(
    output_id: str,
    current_user: User = Depends(get_current_user),

    db: Session = Depends(get_db)
):
    """
    Approve a draft post.
    """
    try:
        output_uuid = uuid.UUID(output_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid output ID format")

    try:
        output = GBPAgentService.approve_post(db, output_uuid)
        return AgentOutputResponse.from_orm(output)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error approving post: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/outputs/{output_id}/reject", response_model=AgentOutputResponse)
async def reject_post(
    output_id: str,
    reason: Optional[str] = None,
    current_user: User = Depends(get_current_user),

    db: Session = Depends(get_db)
):
    """
    Reject a draft post.
    """
    try:
        output_uuid = uuid.UUID(output_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid output ID format")

    try:
        output = GBPAgentService.reject_post(db, output_uuid, reason)
        return AgentOutputResponse.from_orm(output)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error rejecting post: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/outputs/{output_id}", response_model=AgentOutputResponse)
async def update_output(
    output_id: str,
    update: AgentOutputUpdate,
    current_user: User = Depends(get_current_user),

    db: Session = Depends(get_db)
):
    """
    Update an agent output (edit content, change CTA, etc.).
    """
    try:
        output_uuid = uuid.UUID(output_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid output ID format")

    output = db.query(AgentOutput).filter(AgentOutput.id == output_uuid).first()
    if not output:
        raise HTTPException(status_code=404, detail="Output not found")

    try:
        # Update fields if provided
        if update.content is not None:
            output = GBPAgentService.edit_post(
                db=db,
                output_id=output_uuid,
                new_content=update.content,
                new_cta=update.call_to_action
            )
        elif update.status is not None:
            output.status = update.status
            db.commit()
            db.refresh(output)

        # Update other fields
        if update.platform_post_id is not None:
            output.platform_post_id = update.platform_post_id
        if update.platform_url is not None:
            output.platform_url = update.platform_url
        if update.performance_data is not None:
            output.performance_data = update.performance_data
        if update.posted_at is not None:
            output.posted_at = update.posted_at
        if update.scheduled_for is not None:
            output.scheduled_for = update.scheduled_for

        db.commit()
        db.refresh(output)

        return AgentOutputResponse.from_orm(output)

    except Exception as e:
        logger.error(f"Error updating output: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tasks/{location_id}", response_model=AgentTaskListResponse)
async def get_location_tasks(
    location_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all agent tasks for a location.
    """
    try:
        location_uuid = uuid.UUID(location_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid location ID format")

    # Verify location exists
    location = db.query(Location).filter(Location.id == location_uuid).first()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    # Get tasks
    query = db.query(AgentTask).filter(AgentTask.location_id == location_uuid)
    total = query.count()

    tasks = query.order_by(AgentTask.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return AgentTaskListResponse(
        tasks=[AgentTaskResponse.from_orm(task) for task in tasks],
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/tasks/detail/{task_id}", response_model=AgentTaskResponse)
async def get_task(
    task_id: str,
    current_user: User = Depends(get_current_user),

    db: Session = Depends(get_db)
):
    """
    Get a specific task by ID.
    """
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid task ID format")

    task = db.query(AgentTask).filter(AgentTask.id == task_uuid).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return AgentTaskResponse.from_orm(task)


@router.get("/outputs/{location_id}", response_model=AgentOutputListResponse)
async def get_location_outputs(
    location_id: str,
    output_type: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all agent outputs for a location.
    Optionally filter by output type.
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
    query = db.query(AgentOutput).filter(AgentOutput.location_id == location_uuid)

    if output_type:
        query = query.filter(AgentOutput.output_type == output_type)

    total = query.count()

    outputs = query.order_by(AgentOutput.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return AgentOutputListResponse(
        outputs=[AgentOutputResponse.from_orm(output) for output in outputs],
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/outputs/detail/{output_id}", response_model=AgentOutputResponse)
async def get_output(
    output_id: str,
    current_user: User = Depends(get_current_user),

    db: Session = Depends(get_db)
):
    """
    Get a specific output by ID.
    """
    try:
        output_uuid = uuid.UUID(output_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid output ID format")

    output = db.query(AgentOutput).filter(AgentOutput.id == output_uuid).first()
    if not output:
        raise HTTPException(status_code=404, detail="Output not found")

    return AgentOutputResponse.from_orm(output)
