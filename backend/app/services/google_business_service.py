"""
Google Business Profile API Service.
Handles posting to GBP and fetching metrics.
"""

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from app.services.google_oauth_service import GoogleOAuthService
from app.models.agent_output import GBPCallToAction
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class GoogleBusinessService:
    """Service for Google My Business API operations."""

    @staticmethod
    def create_local_post(
        db: Session,
        location_id: str,
        gbp_location_name: str,
        content: str,
        call_to_action: GBPCallToAction,
        media_urls: Optional[List[str]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Create a local post on Google Business Profile.

        Args:
            db: Database session
            location_id: Our location UUID
            gbp_location_name: Google's location resource name (e.g., 'locations/123')
            content: Post content text
            call_to_action: Call to action type
            media_urls: Optional list of image URLs

        Returns:
            Created post dict or None on failure
        """
        # Get valid credentials
        credentials = GoogleOAuthService.get_valid_credentials(db, location_id)
        if not credentials:
            logger.error(f"No valid Google credentials for location {location_id}")
            return None

        try:
            service = build('mybusiness', 'v4', credentials=credentials)

            # Build local post object
            local_post = {
                "summary": content,
                "callToAction": {
                    "actionType": call_to_action.value
                }
            }

            # Add media if provided
            if media_urls:
                local_post["media"] = [
                    {
                        "mediaFormat": "PHOTO",
                        "sourceUrl": url
                    }
                    for url in media_urls
                ]

            # Create the post
            result = service.accounts().locations().localPosts().create(
                parent=gbp_location_name,
                body=local_post
            ).execute()

            logger.info(f"Successfully created GBP post for location {gbp_location_name}")
            return result

        except HttpError as e:
            logger.error(f"HTTP error creating GBP post: {e.status_code} - {e.reason}")
            logger.error(f"Error details: {e.content}")
            return None
        except Exception as e:
            logger.error(f"Failed to create GBP post: {str(e)}")
            return None

    @staticmethod
    def get_location_insights(
        db: Session,
        location_id: str,
        gbp_location_name: str,
        start_date: datetime,
        end_date: datetime
    ) -> Optional[Dict[str, Any]]:
        """
        Get insights/metrics for a Google Business Profile location.

        Args:
            db: Database session
            location_id: Our location UUID
            gbp_location_name: Google's location resource name
            start_date: Start date for metrics
            end_date: End date for metrics

        Returns:
            Insights dict or None
        """
        credentials = GoogleOAuthService.get_valid_credentials(db, location_id)
        if not credentials:
            logger.error(f"No valid Google credentials for location {location_id}")
            return None

        try:
            service = build('mybusiness', 'v4', credentials=credentials)

            # Format dates
            start_time = start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
            end_time = end_date.strftime('%Y-%m-%dT%H:%M:%SZ')

            # Request location insights
            request_body = {
                "locationNames": [gbp_location_name],
                "basicRequest": {
                    "metricRequests": [
                        {"metric": "QUERIES_DIRECT"},
                        {"metric": "QUERIES_INDIRECT"},
                        {"metric": "VIEWS_MAPS"},
                        {"metric": "VIEWS_SEARCH"},
                        {"metric": "ACTIONS_WEBSITE"},
                        {"metric": "ACTIONS_PHONE"},
                        {"metric": "ACTIONS_DRIVING_DIRECTIONS"},
                    ],
                    "timeRange": {
                        "startTime": start_time,
                        "endTime": end_time
                    }
                }
            }

            result = service.accounts().locations().reportInsights(
                name=gbp_location_name,
                body=request_body
            ).execute()

            logger.info(f"Successfully fetched insights for location {gbp_location_name}")
            return result

        except HttpError as e:
            logger.error(f"HTTP error fetching GBP insights: {e.status_code} - {e.reason}")
            return None
        except Exception as e:
            logger.error(f"Failed to fetch GBP insights: {str(e)}")
            return None

    @staticmethod
    def get_reviews(
        db: Session,
        location_id: str,
        gbp_location_name: str
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get reviews for a Google Business Profile location.

        Args:
            db: Database session
            location_id: Our location UUID
            gbp_location_name: Google's location resource name

        Returns:
            List of review dicts or None
        """
        credentials = GoogleOAuthService.get_valid_credentials(db, location_id)
        if not credentials:
            logger.error(f"No valid Google credentials for location {location_id}")
            return None

        try:
            service = build('mybusiness', 'v4', credentials=credentials)

            result = service.accounts().locations().reviews().list(
                parent=gbp_location_name
            ).execute()

            reviews = result.get('reviews', [])
            logger.info(f"Fetched {len(reviews)} reviews for location {gbp_location_name}")
            return reviews

        except HttpError as e:
            logger.error(f"HTTP error fetching reviews: {e.status_code} - {e.reason}")
            return None
        except Exception as e:
            logger.error(f"Failed to fetch reviews: {str(e)}")
            return None

    @staticmethod
    def reply_to_review(
        db: Session,
        location_id: str,
        gbp_location_name: str,
        review_name: str,
        reply_text: str
    ) -> Optional[Dict[str, Any]]:
        """
        Reply to a Google Business Profile review.

        Args:
            db: Database session
            location_id: Our location UUID
            gbp_location_name: Google's location resource name
            review_name: Review resource name
            reply_text: Reply content

        Returns:
            Reply result or None
        """
        credentials = GoogleOAuthService.get_valid_credentials(db, location_id)
        if not credentials:
            logger.error(f"No valid Google credentials for location {location_id}")
            return None

        try:
            service = build('mybusiness', 'v4', credentials=credentials)

            reply_body = {
                "comment": reply_text
            }

            result = service.accounts().locations().reviews().updateReply(
                name=review_name,
                body=reply_body
            ).execute()

            logger.info(f"Successfully replied to review {review_name}")
            return result

        except HttpError as e:
            logger.error(f"HTTP error replying to review: {e.status_code} - {e.reason}")
            return None
        except Exception as e:
            logger.error(f"Failed to reply to review: {str(e)}")
            return None

    @staticmethod
    def parse_insights_response(insights: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse Google My Business insights response into simplified metrics.

        Args:
            insights: Raw insights response from API

        Returns:
            Simplified metrics dict
        """
        metrics = {
            "calls": 0,
            "gbpViews": 0,
            "directionRequests": 0,
            "websiteClicks": 0,
            "queries": {
                "direct": 0,
                "indirect": 0
            }
        }

        try:
            location_metrics = insights.get('locationMetrics', [])
            if not location_metrics:
                return metrics

            metric_values = location_metrics[0].get('metricValues', [])

            for metric in metric_values:
                metric_type = metric.get('metric')
                total_value = metric.get('totalValue', {})
                value = total_value.get('value', 0)

                if metric_type == 'ACTIONS_PHONE':
                    metrics['calls'] = int(value)
                elif metric_type in ['VIEWS_MAPS', 'VIEWS_SEARCH']:
                    metrics['gbpViews'] += int(value)
                elif metric_type == 'ACTIONS_DRIVING_DIRECTIONS':
                    metrics['directionRequests'] = int(value)
                elif metric_type == 'ACTIONS_WEBSITE':
                    metrics['websiteClicks'] = int(value)
                elif metric_type == 'QUERIES_DIRECT':
                    metrics['queries']['direct'] = int(value)
                elif metric_type == 'QUERIES_INDIRECT':
                    metrics['queries']['indirect'] = int(value)

        except Exception as e:
            logger.error(f"Error parsing insights: {str(e)}")

        return metrics
