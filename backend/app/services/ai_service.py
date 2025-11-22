"""
AI Service using Anthropic Claude API.
Handles all AI content generation for agents.
"""

import anthropic
from app.config import settings
from app.models import Location
from app.models.agent_output import GBPCallToAction
from typing import Dict, Any, List, Optional
import logging
import json

logger = logging.getLogger(__name__)

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY) if settings.ANTHROPIC_API_KEY else None


class AIService:
    """Service for AI-powered content generation using Claude."""

    @staticmethod
    def generate_gbp_post(
        location: Location,
        context: Optional[str] = None,
        previous_posts: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Generate a Google Business Profile post using AI.

        Args:
            location: The business location
            context: Optional additional context for generation
            previous_posts: Optional list of recent posts to avoid repetition

        Returns:
            Dict with 'content', 'cta', and 'reasoning'
        """
        if not client:
            logger.warning("Anthropic API key not configured, using mock data")
            return AIService._generate_mock_gbp_post(location)

        try:
            # Build the prompt
            prompt = AIService._build_gbp_prompt(location, context, previous_posts)

            # Call Claude API
            message = client.messages.create(
                model="claude-sonnet-4-20250514",  # Latest Sonnet model
                max_tokens=1024,
                temperature=0.7,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Extract response
            response_text = message.content[0].text

            # Parse JSON response
            try:
                result = json.loads(response_text)
                logger.info(f"Generated GBP post for {location.business_name}")
                return result
            except json.JSONDecodeError:
                logger.error(f"Failed to parse JSON response: {response_text}")
                return AIService._generate_mock_gbp_post(location)

        except Exception as e:
            logger.error(f"Error generating GBP post: {str(e)}")
            return AIService._generate_mock_gbp_post(location)

    @staticmethod
    def _build_gbp_prompt(
        location: Location,
        context: Optional[str],
        previous_posts: Optional[List[str]]
    ) -> str:
        """Build the prompt for GBP post generation."""

        services_list = ""
        if location.services:
            try:
                services = json.loads(location.services) if isinstance(location.services, str) else location.services
                services_list = ", ".join(services)
            except:
                services_list = str(location.services)

        prompt = f"""You are a local SEO expert creating Google Business Profile posts for businesses.

Business Context:
- Business Name: {location.business_name}
- Category: {location.primary_category}
- Services: {services_list}
- Brand Tone: {location.brand_tone or 'professional and friendly'}
- Location: {location.city}, {location.state}
- Primary Goal: {location.primary_goal or 'increase engagement'}

"""

        if context:
            prompt += f"\nAdditional Context: {context}\n"

        if previous_posts:
            prompt += f"\nRecent Posts (avoid repetition):\n"
            for i, post in enumerate(previous_posts[:3], 1):
                prompt += f"{i}. {post}\n"

        prompt += """
Create a compelling Google Business Profile post that:
1. Highlights one of their services or a current offering
2. Uses their brand tone
3. Includes a clear call-to-action
4. Is between 100-300 characters (concise and engaging)
5. Optimized for local search visibility
6. Avoids being overly promotional or salesy

Return ONLY a JSON object in this exact format (no markdown, no extra text):
{
  "content": "post text here",
  "cta": "CALL" | "BOOK" | "ORDER" | "LEARN_MORE" | "SIGN_UP" | "SHOP",
  "reasoning": "brief explanation of why this post will work"
}
"""

        return prompt

    @staticmethod
    def _generate_mock_gbp_post(location: Location) -> Dict[str, Any]:
        """Generate a mock GBP post when AI is not available."""
        return {
            "content": f"Quality {location.primary_category} services in {location.city}! We're dedicated to excellence and customer satisfaction. Visit us today!",
            "cta": "CALL",
            "reasoning": "Mock post highlighting local presence and service quality with a clear call-to-action."
        }

    @staticmethod
    def generate_blog_post(
        location: Location,
        topic: str,
        keywords: Optional[List[str]] = None,
        word_count: int = 800
    ) -> Dict[str, Any]:
        """
        Generate a blog post using AI.

        Args:
            location: The business location
            topic: Topic for the blog post
            keywords: Optional list of keywords to target
            word_count: Target word count

        Returns:
            Dict with 'title', 'content', 'meta_description', and 'reasoning'
        """
        if not client:
            logger.warning("Anthropic API key not configured, using mock data")
            return AIService._generate_mock_blog_post(location, topic)

        try:
            prompt = AIService._build_blog_prompt(location, topic, keywords, word_count)

            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,  # Longer for blog posts
                temperature=0.7,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            response_text = message.content[0].text

            try:
                result = json.loads(response_text)
                logger.info(f"Generated blog post for {location.business_name}: {topic}")
                return result
            except json.JSONDecodeError:
                logger.error(f"Failed to parse JSON response: {response_text}")
                return AIService._generate_mock_blog_post(location, topic)

        except Exception as e:
            logger.error(f"Error generating blog post: {str(e)}")
            return AIService._generate_mock_blog_post(location, topic)

    @staticmethod
    def _build_blog_prompt(
        location: Location,
        topic: str,
        keywords: Optional[List[str]],
        word_count: int
    ) -> str:
        """Build prompt for blog post generation."""

        prompt = f"""You are a professional content writer specializing in local SEO.

Business Context:
- Business Name: {location.business_name}
- Category: {location.primary_category}
- Location: {location.city}, {location.state}
- Brand Tone: {location.brand_tone or 'professional and informative'}

Blog Post Requirements:
- Topic: {topic}
- Target Word Count: {word_count} words
- Target Keywords: {', '.join(keywords) if keywords else 'natural language optimization'}

Create a high-quality blog post that:
1. Provides genuine value to readers
2. Incorporates target keywords naturally
3. Maintains the brand's tone
4. Includes local context relevant to {location.city}
5. Is optimized for SEO without keyword stuffing
6. Has a compelling title and meta description

Return ONLY a JSON object in this exact format (no markdown):
{{
  "title": "SEO-optimized blog post title",
  "content": "full blog post content in markdown format",
  "meta_description": "155-character meta description",
  "reasoning": "brief explanation of the SEO strategy"
}}
"""

        return prompt

    @staticmethod
    def _generate_mock_blog_post(location: Location, topic: str) -> Dict[str, Any]:
        """Generate a mock blog post when AI is not available."""
        return {
            "title": f"{topic} - {location.business_name}",
            "content": f"# {topic}\n\nWelcome to our latest blog post about {topic}. At {location.business_name}, we're committed to providing you with valuable information.\n\n## Why This Matters\n\nThis topic is important for our community in {location.city}...\n\n## Conclusion\n\nThank you for reading! Contact us to learn more.",
            "meta_description": f"Learn about {topic} from {location.business_name}, serving {location.city} and surrounding areas.",
            "reasoning": "Mock blog post structure with proper SEO elements."
        }

    @staticmethod
    def generate_review_response(
        location: Location,
        review_text: str,
        review_rating: int
    ) -> Dict[str, Any]:
        """
        Generate a response to a customer review.

        Args:
            location: The business location
            review_text: The review content
            review_rating: Star rating (1-5)

        Returns:
            Dict with 'response' and 'reasoning'
        """
        if not client:
            logger.warning("Anthropic API key not configured, using mock data")
            return AIService._generate_mock_review_response(location, review_rating)

        try:
            prompt = f"""You are responding to a customer review for {location.business_name}.

Business: {location.business_name}
Location: {location.city}, {location.state}
Brand Tone: {location.brand_tone or 'professional and appreciative'}

Review Rating: {review_rating}/5 stars
Review Text: {review_text}

Generate a personalized, authentic response that:
1. Thanks the customer for their feedback
2. Addresses specific points they mentioned
3. Maintains the brand tone
4. Is appropriate for the rating (positive/negative)
5. Is between 50-150 words
6. Feels genuine, not templated

Return ONLY a JSON object:
{{
  "response": "the review response text",
  "reasoning": "brief explanation of the approach"
}}
"""

            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=512,
                temperature=0.8,  # Slightly higher for more natural responses
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = message.content[0].text
            result = json.loads(response_text)
            logger.info(f"Generated review response for {location.business_name}")
            return result

        except Exception as e:
            logger.error(f"Error generating review response: {str(e)}")
            return AIService._generate_mock_review_response(location, review_rating)

    @staticmethod
    def _generate_mock_review_response(location: Location, rating: int) -> Dict[str, Any]:
        """Generate a mock review response when AI is not available."""
        if rating >= 4:
            response = f"Thank you so much for your wonderful review! We're thrilled to hear about your positive experience with {location.business_name}. We look forward to serving you again soon!"
        else:
            response = f"Thank you for your feedback. We take all reviews seriously and would love the opportunity to make things right. Please contact us directly so we can address your concerns."

        return {
            "response": response,
            "reasoning": "Mock response based on rating sentiment."
        }
