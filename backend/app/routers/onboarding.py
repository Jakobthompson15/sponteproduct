"""
Onboarding API endpoints.
Handles onboarding form submission and user/location creation.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.onboarding import OnboardingSubmitRequest, OnboardingSubmitResponse
from app.models import User, Location, AgentConfig, AgentType, AutonomyMode, SubscriptionTier
from app.services.email_service import send_welcome_email
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel
from typing import Optional, List, Union
import logging

router = APIRouter(prefix="/api/onboarding", tags=["Onboarding"])
logger = logging.getLogger(__name__)


class BusinessProfileRequest(BaseModel):
    """Schema for creating a draft location after step 1."""
    businessName: str
    dbaName: Optional[str] = None
    streetAddress: str
    city: str
    state: str
    zipCode: str
    phone: str
    phoneSecondary: Optional[str] = None
    websiteUrl: Optional[str] = None
    cmsPlatform: Optional[str] = None
    primaryCategory: str
    services: Optional[Union[str, List[str]]] = None


class BusinessProfileResponse(BaseModel):
    """Response after creating draft location."""
    success: bool
    location_id: str
    message: str


@router.post("/create-location", response_model=BusinessProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_draft_location(
    business_data: BusinessProfileRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a draft location after step 1 (Business Profile).
    This allows users to connect OAuth accounts in step 2.

    If a location already exists for this user, it will be updated instead.
    """
    try:
        # Parse services
        services_list = []
        if business_data.services:
            if isinstance(business_data.services, str):
                services_list = [s.strip() for s in business_data.services.split('\n') if s.strip()]
            else:
                services_list = business_data.services

        # Check if user already has a location (draft or complete)
        existing_location = db.query(Location).filter(Location.user_id == current_user.id).first()

        if existing_location:
            # Update existing location with new business profile data
            existing_location.business_name = business_data.businessName
            existing_location.dba_name = business_data.dbaName
            existing_location.street_address = business_data.streetAddress
            existing_location.city = business_data.city
            existing_location.state = business_data.state
            existing_location.zip_code = business_data.zipCode
            existing_location.phone_primary = business_data.phone
            existing_location.phone_secondary = business_data.phoneSecondary
            existing_location.website_url = business_data.websiteUrl
            existing_location.cms_platform = business_data.cmsPlatform
            existing_location.primary_category = business_data.primaryCategory
            existing_location.services = services_list

            db.commit()
            db.refresh(existing_location)

            logger.info(f"Updated existing location {existing_location.id} for user {current_user.email}")

            return BusinessProfileResponse(
                success=True,
                location_id=str(existing_location.id),
                message="Business profile updated successfully"
            )

        # Create new draft location
        location = Location(
            user_id=current_user.id,
            business_name=business_data.businessName,
            dba_name=business_data.dbaName,
            street_address=business_data.streetAddress,
            city=business_data.city,
            state=business_data.state,
            zip_code=business_data.zipCode,
            phone_primary=business_data.phone,
            phone_secondary=business_data.phoneSecondary,
            website_url=business_data.websiteUrl,
            cms_platform=business_data.cmsPlatform,
            primary_category=business_data.primaryCategory,
            services=services_list
            # Other fields (brand_tone, cadence, etc.) will be filled in at final submission
        )

        db.add(location)
        db.commit()
        db.refresh(location)

        logger.info(f"Created draft location {location.id} for user {current_user.email}")

        return BusinessProfileResponse(
            success=True,
            location_id=str(location.id),
            message="Business profile created successfully"
        )

    except Exception as e:
        db.rollback()
        logger.error(f"Error creating draft location: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create business profile: {str(e)}"
        )


@router.post("/submit", response_model=OnboardingSubmitResponse, status_code=status.HTTP_201_CREATED)
async def submit_onboarding(
    onboarding_data: OnboardingSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit onboarding form data.
    Requires Clerk authentication.

    Creates:
    1. User account (if doesn't exist) - synced with Clerk
    2. Business location with NAP data
    3. Default agent configs (6 agents in draft mode)

    Returns:
    - user_id: UUID of created user
    - location_id: UUID of created location
    - next_steps: List of actions user should take
    """
    try:
        # Use the authenticated user from Clerk
        user = current_user

        # Update onboarding status
        if not user.onboarding_completed:
            user.onboarding_completed = True
            db.add(user)
            logger.info(f"Marked onboarding complete for user: {user.email}")

        # Parse services from newline-separated string to list
        services_list = []
        if onboarding_data.services:
            if isinstance(onboarding_data.services, str):
                services_list = [s.strip() for s in onboarding_data.services.split('\n') if s.strip()]
            else:
                services_list = onboarding_data.services

        # Check if location already exists (created during step 1)
        location = db.query(Location).filter(Location.user_id == user.id).first()

        if location:
            # Update existing draft location with complete data
            location.business_name = onboarding_data.businessName
            location.dba_name = onboarding_data.dbaName
            location.street_address = onboarding_data.streetAddress
            location.city = onboarding_data.city
            location.state = onboarding_data.state
            location.zip_code = onboarding_data.zipCode
            location.phone_primary = onboarding_data.phone
            location.phone_secondary = onboarding_data.phoneSecondary
            location.website_url = onboarding_data.websiteUrl
            location.cms_platform = onboarding_data.cmsPlatform
            location.primary_category = onboarding_data.primaryCategory
            location.services = services_list
            location.brand_tone = onboarding_data.brandTone
            location.blog_cadence = onboarding_data.blogCadence
            location.gbp_cadence = onboarding_data.gbpCadence
            location.forbidden_words = onboarding_data.forbiddenWords
            location.forbidden_topics = onboarding_data.forbiddenTopics
            location.primary_goal = onboarding_data.primaryGoal
            location.report_frequency = onboarding_data.reportFrequency
            location.report_emails = onboarding_data.reportEmails

            logger.info(f"Updated existing location: {location.business_name} in {location.city}, {location.state}")
        else:
            # Create new location (if user skipped step 1's draft creation somehow)
            location = Location(
                user_id=user.id,
                business_name=onboarding_data.businessName,
                dba_name=onboarding_data.dbaName,
                street_address=onboarding_data.streetAddress,
                city=onboarding_data.city,
                state=onboarding_data.state,
                zip_code=onboarding_data.zipCode,
                phone_primary=onboarding_data.phone,
                phone_secondary=onboarding_data.phoneSecondary,
                website_url=onboarding_data.websiteUrl,
                cms_platform=onboarding_data.cmsPlatform,
                primary_category=onboarding_data.primaryCategory,
                services=services_list,
                brand_tone=onboarding_data.brandTone,
                blog_cadence=onboarding_data.blogCadence,
                gbp_cadence=onboarding_data.gbpCadence,
                forbidden_words=onboarding_data.forbiddenWords,
                forbidden_topics=onboarding_data.forbiddenTopics,
                primary_goal=onboarding_data.primaryGoal,
                report_frequency=onboarding_data.reportFrequency,
                report_emails=onboarding_data.reportEmails
            )
            db.add(location)
            logger.info(f"Created new location: {location.business_name} in {location.city}, {location.state}")

        db.flush()  # Get location.id without committing

        # Determine autonomy mode from global setting
        autonomy_mode = AutonomyMode.DRAFT  # Default
        if onboarding_data.globalAutonomy:
            try:
                # Handle legacy 'approve' and 'auto' values by converting them
                mode_value = onboarding_data.globalAutonomy.lower()
                if mode_value in ['approve', 'auto']:
                    # Convert legacy 'approve' to 'draft' (manual control)
                    # Convert legacy 'auto' to 'autopilot'
                    mode_value = 'draft' if mode_value == 'approve' else 'autopilot'
                    logger.info(f"Converted legacy autonomy mode '{onboarding_data.globalAutonomy}' to '{mode_value}'")

                autonomy_mode = AutonomyMode(mode_value)
            except ValueError:
                logger.warning(f"Invalid autonomy mode '{onboarding_data.globalAutonomy}', defaulting to DRAFT")
                autonomy_mode = AutonomyMode.DRAFT

        # Create agent configs for all 6 agents
        agents_to_create = [
            AgentType.GBP,
            AgentType.NAP,
            AgentType.KEYWORD,
            AgentType.BLOG,
            AgentType.SOCIAL,
            AgentType.REPORTING
        ]

        for agent_type in agents_to_create:
            agent_config = AgentConfig(
                location_id=location.id,
                agent_type=agent_type,
                autonomy_mode=autonomy_mode,
                is_active=True,
                config_data={}  # Will be populated later based on agent type
            )
            db.add(agent_config)

        logger.info(f"Created {len(agents_to_create)} agent configs for location {location.id}")

        # Commit all changes
        db.commit()
        db.refresh(user)
        db.refresh(location)

        # Send welcome email
        try:
            send_welcome_email(
                user_email=user.email,
                business_name=location.business_name,
                user_id=str(user.id),
                location_id=str(location.id)
            )
            logger.info(f"Welcome email queued for {user.email}")
        except Exception as email_error:
            # Log but don't fail the request if email fails
            logger.error(f"Failed to send welcome email: {str(email_error)}")

        # Return success response
        return OnboardingSubmitResponse(
            success=True,
            message="Onboarding completed successfully! Check your email for next steps.",
            user_id=str(user.id),
            location_id=str(location.id),
            next_steps=[
                "Check your email for a welcome message",
                "Connect your Google Business Profile",
                "Connect your Google Search Console",
                "Connect your WordPress site (if applicable)",
                "Review your agent settings in the dashboard"
            ]
        )

    except IntegrityError as e:
        db.rollback()
        logger.error(f"Database integrity error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists or invalid data provided"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Error during onboarding: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during onboarding: {str(e)}"
        )
