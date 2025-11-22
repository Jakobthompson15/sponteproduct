"""
Locations API endpoints.
Handles location-related operations including GBP configuration.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models import Location, User
from pydantic import BaseModel
import uuid
import logging

router = APIRouter(prefix="/api/locations", tags=["Locations"])
logger = logging.getLogger(__name__)


class GBPLocationUpdate(BaseModel):
    """Schema for updating GBP location name."""
    gbp_location_name: str


class LocationResponse(BaseModel):
    """Schema for location response."""
    id: str
    business_name: str


@router.get("/me", response_model=LocationResponse | None)
async def get_my_location(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get the current user's location.

    Returns:
        Location data or None if user hasn't completed onboarding
    """
    location = db.query(Location).filter(Location.user_id == current_user.id).first()

    if not location:
        return None

    return LocationResponse(
        id=str(location.id),
        business_name=location.business_name or ""
    )


@router.patch("/{location_id}/gbp-location")
async def save_gbp_location(
    location_id: str,
    data: GBPLocationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Save the selected Google Business Profile location name to a location.

    Args:
        location_id: Location UUID
        data: GBP location name (resource name from Google)

    Returns:
        Success message
    """
    try:
        location_uuid = uuid.UUID(location_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid location ID format")

    # Get location
    location = db.query(Location).filter(Location.id == location_uuid).first()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    # Update GBP location name
    location.gbp_location_name = data.gbp_location_name
    db.commit()
    db.refresh(location)

    logger.info(f"Saved GBP location for {location_id}: {data.gbp_location_name}")

    return {
        "message": "GBP location saved successfully",
        "location_id": str(location.id),
        "gbp_location_name": location.gbp_location_name
    }


@router.get("/{location_id}")
async def get_location(
    location_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get location details.

    Args:
        location_id: Location UUID

    Returns:
        Location data
    """
    try:
        location_uuid = uuid.UUID(location_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid location ID format")

    location = db.query(Location).filter(Location.id == location_uuid).first()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    return {
        "id": str(location.id),
        "business_name": location.business_name,
        "city": location.city,
        "state": location.state,
        "gbp_location_name": location.gbp_location_name,
        "gbp_cadence": location.gbp_cadence,
        "blog_cadence": location.blog_cadence,
    }
