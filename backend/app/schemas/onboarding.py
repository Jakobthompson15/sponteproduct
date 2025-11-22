"""
Pydantic schemas for onboarding API requests and responses.
"""

from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List, Union
from datetime import datetime


class OnboardingSubmitRequest(BaseModel):
    """
    Schema for onboarding form submission.
    Matches the fields collected in onboarding.html
    """

    # Step 1: Business Profile & NAP
    businessName: str  # Legal business name
    dbaName: Optional[str] = None  # "Doing Business As" name
    streetAddress: str
    city: str
    state: str
    zipCode: str
    phone: str  # Primary phone
    phoneSecondary: Optional[str] = None
    websiteUrl: Optional[str] = None
    cmsPlatform: Optional[str] = None  # wordpress, shopify, wix, etc.
    primaryCategory: str  # e.g., "Pizza Restaurant", "Dentist"
    services: Optional[Union[str, List[str]]] = None  # Newline-separated string or array of services

    # Step 2: Connect Accounts (OAuth will be handled separately)
    # This step is done after onboarding via dashboard

    # Step 3: Content & Brand
    brandTone: Optional[str] = None  # professional, casual, friendly, etc.
    blogCadence: Optional[str] = None  # weekly, biweekly, monthly
    gbpCadence: Optional[str] = None  # daily, weekly, biweekly
    forbiddenWords: Optional[str] = None  # Comma-separated
    forbiddenTopics: Optional[str] = None  # Comma-separated

    # Step 4: Autonomy & Control
    globalAutonomy: Optional[str] = "draft"  # draft or autopilot

    # Step 5: Goals & Reporting
    primaryGoal: Optional[str] = None  # more_calls, more_traffic, more_reviews, etc.
    reportFrequency: Optional[str] = "weekly"  # weekly, monthly
    reportEmails: Optional[str] = None  # Comma-separated email list

    # User email (we'll add this to the form later, or generate from OAuth)
    email: EmailStr

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        """Ensure email is provided and valid."""
        if not v:
            raise ValueError('Email is required')
        return v.lower()

    @field_validator('services', mode='before')
    @classmethod
    def parse_services(cls, v):
        """Convert newline-separated services to JSON array, or pass through if already a list."""
        if v and isinstance(v, str):
            return [s.strip() for s in v.split('\n') if s.strip()]
        elif v and isinstance(v, list):
            return [s.strip() for s in v if s.strip()]
        return v

    class Config:
        extra = "ignore"  # Ignore extra fields from frontend
        json_schema_extra = {
            "example": {
                "email": "owner@example.com",
                "businessName": "Tony's Pizzeria LLC",
                "dbaName": "Tony's Pizza",
                "streetAddress": "123 Main Street",
                "city": "Chicago",
                "state": "IL",
                "zipCode": "60601",
                "phone": "(312) 555-1234",
                "websiteUrl": "https://tonyspizza.com",
                "cmsPlatform": "wordpress",
                "primaryCategory": "Pizza Restaurant",
                "services": "Dine-in\\nTakeout\\nDelivery",
                "brandTone": "friendly",
                "blogCadence": "weekly",
                "gbpCadence": "weekly",
                "globalAutonomy": "draft",
                "primaryGoal": "more_calls",
                "reportFrequency": "weekly",
                "reportEmails": "owner@example.com"
            }
        }


class OnboardingSubmitResponse(BaseModel):
    """
    Response after successful onboarding submission.
    """
    success: bool
    message: str
    user_id: str
    location_id: str
    next_steps: List[str]

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Onboarding completed successfully!",
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "location_id": "660e8400-e29b-41d4-a716-446655440001",
                "next_steps": [
                    "Check your email for next steps",
                    "Connect your Google Business Profile",
                    "Connect your WordPress site",
                    "Review your agent settings"
                ]
            }
        }
