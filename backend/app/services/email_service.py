"""
Email service using Resend API.
Handles sending transactional emails (welcome, notifications, reports).
"""

import resend
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Initialize Resend with API key
resend.api_key = settings.RESEND_API_KEY


def send_welcome_email(user_email: str, business_name: str, user_id: str, location_id: str):
    """
    Send welcome email when user completes onboarding.

    Args:
        user_email: User's email address
        business_name: Legal business name
        user_id: UUID of created user
        location_id: UUID of created location
    """
    try:
        response = resend.Emails.send({
            "from": "Sponte AI <onboarding@resend.dev>",  # Change to your verified domain later
            "to": user_email,
            "subject": f"Welcome to Sponte AI - Your Agents Are Ready!",
            "html": get_welcome_email_html(business_name, user_id, location_id)
        })

        logger.info(f"Welcome email sent to {user_email}. Email ID: {response.get('id')}")
        return response

    except Exception as e:
        logger.error(f"Failed to send welcome email to {user_email}: {str(e)}")
        # Don't raise - email failure shouldn't block onboarding
        return None


def send_report_email(
    recipient_emails: str,
    business_name: str,
    report_type: str,
    report_data: dict,
    report_id: str
):
    """
    Send weekly or monthly report email.

    Args:
        recipient_emails: Comma-separated email addresses
        business_name: Business name for personalization
        report_type: 'weekly' or 'monthly'
        report_data: Report data dict with metrics, insights, etc.
        report_id: UUID of the report for viewing link
    """
    try:
        # Parse recipient emails
        recipients = [email.strip() for email in recipient_emails.split(',')]

        subject = f"{'Weekly' if report_type == 'weekly' else 'Monthly'} Report: {business_name}"

        response = resend.Emails.send({
            "from": "Sponte AI <reports@resend.dev>",  # Change to your verified domain later
            "to": recipients,
            "subject": subject,
            "html": get_report_email_html(business_name, report_type, report_data, report_id)
        })

        logger.info(f"{report_type.capitalize()} report email sent to {recipient_emails}. Email ID: {response.get('id')}")
        return response

    except Exception as e:
        logger.error(f"Failed to send {report_type} report email to {recipient_emails}: {str(e)}")
        raise  # Raise here so we can track email failures in reports


def get_welcome_email_html(business_name: str, user_id: str, location_id: str) -> str:
    """
    Generate HTML for welcome email.
    Beautiful, modern design with improved visual hierarchy and styling.
    """
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
                line-height: 1.6;
                color: #1A1D2E;
                background: linear-gradient(135deg, #f5f7fa 0%, #e8eef3 100%);
                margin: 0;
                padding: 20px;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background: white;
                border-radius: 16px;
                overflow: hidden;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.12);
            }}
            .header {{
                background: linear-gradient(135deg, #FF5810 0%, #FF3D00 100%);
                color: white;
                padding: 50px 40px;
                text-align: center;
                position: relative;
            }}
            .header::after {{
                content: '';
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                height: 4px;
                background: linear-gradient(90deg, rgba(255,255,255,0.3) 0%, rgba(255,255,255,0) 100%);
            }}
            .header h1 {{
                margin: 0 0 10px 0;
                font-size: 36px;
                font-weight: 700;
                letter-spacing: -0.5px;
            }}
            .header p {{
                margin: 0;
                font-size: 16px;
                opacity: 0.95;
                font-weight: 400;
            }}
            .content {{
                padding: 45px 40px;
            }}
            .greeting {{
                font-size: 24px;
                font-weight: 700;
                margin-bottom: 15px;
                color: #1A1D2E;
                line-height: 1.3;
            }}
            .intro {{
                font-size: 16px;
                color: #4B5563;
                margin-bottom: 35px;
                line-height: 1.7;
            }}
            .section-title {{
                font-size: 18px;
                font-weight: 700;
                color: #1A1D2E;
                margin: 35px 0 20px 0;
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            .section-title .emoji {{
                font-size: 24px;
            }}
            .agent-grid {{
                display: grid;
                gap: 16px;
                margin: 25px 0;
            }}
            .agent-card {{
                background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
                border: 2px solid #e5e7eb;
                border-radius: 12px;
                padding: 20px;
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
            }}
            .agent-card::before {{
                content: '';
                position: absolute;
                left: 0;
                top: 0;
                bottom: 0;
                width: 4px;
                background: linear-gradient(180deg, #FF5810 0%, #FF3D00 100%);
            }}
            .agent-card-header {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 8px;
            }}
            .agent-name {{
                font-size: 16px;
                font-weight: 700;
                color: #1A1D2E;
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            .agent-icon {{
                font-size: 20px;
            }}
            .agent-description {{
                font-size: 14px;
                color: #6B7280;
                margin: 0;
                line-height: 1.5;
                padding-left: 30px;
            }}
            .badge {{
                display: inline-block;
                background: #1A1D2E;
                color: white;
                padding: 4px 10px;
                border-radius: 6px;
                font-size: 11px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.8px;
            }}
            .cta-section {{
                background: linear-gradient(135deg, #fff4ed 0%, #ffe8d6 100%);
                border: 3px solid #FF5810;
                border-radius: 12px;
                padding: 30px;
                margin: 35px 0;
                text-align: center;
            }}
            .cta-section h3 {{
                margin: 0 0 10px 0;
                font-size: 20px;
                color: #1A1D2E;
                font-weight: 700;
            }}
            .cta-section p {{
                margin: 0 0 20px 0;
                color: #6B7280;
                font-size: 15px;
            }}
            .cta-button {{
                display: inline-block;
                background: linear-gradient(135deg, #FF5810 0%, #FF3D00 100%);
                color: white;
                padding: 16px 40px;
                text-decoration: none;
                border-radius: 10px;
                font-weight: 700;
                font-size: 16px;
                box-shadow: 0 4px 15px rgba(255, 88, 16, 0.3);
                transition: all 0.3s ease;
                letter-spacing: 0.3px;
            }}
            .steps-list {{
                background: white;
                border: 2px solid #e5e7eb;
                border-radius: 12px;
                padding: 25px 25px 25px 45px;
                margin: 25px 0;
            }}
            .steps-list ol {{
                margin: 0;
                padding: 0;
                counter-reset: step-counter;
                list-style: none;
            }}
            .steps-list li {{
                margin: 18px 0;
                color: #1A1D2E;
                font-size: 15px;
                line-height: 1.6;
                position: relative;
                padding-left: 10px;
                counter-increment: step-counter;
            }}
            .steps-list li::before {{
                content: counter(step-counter);
                position: absolute;
                left: -35px;
                top: 0;
                background: linear-gradient(135deg, #FF5810 0%, #FF3D00 100%);
                color: white;
                width: 26px;
                height: 26px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 700;
                font-size: 13px;
            }}
            .steps-list strong {{
                color: #1A1D2E;
                font-weight: 700;
            }}
            .help-section {{
                margin-top: 40px;
                padding-top: 30px;
                border-top: 2px solid #e5e7eb;
                text-align: center;
            }}
            .help-section h4 {{
                margin: 0 0 8px 0;
                font-size: 16px;
                color: #1A1D2E;
                font-weight: 700;
            }}
            .help-section p {{
                margin: 5px 0;
                color: #6B7280;
                font-size: 14px;
                line-height: 1.6;
            }}
            .footer {{
                background: linear-gradient(135deg, #1A1D2E 0%, #2d3748 100%);
                padding: 35px 40px;
                text-align: center;
                color: #9CA3AF;
            }}
            .footer-logo {{
                font-size: 22px;
                font-weight: 800;
                color: white;
                margin-bottom: 8px;
                letter-spacing: -0.5px;
            }}
            .footer-tagline {{
                font-size: 13px;
                color: #9CA3AF;
                margin-bottom: 20px;
            }}
            .footer-ids {{
                font-size: 11px;
                color: #6B7280;
                margin-top: 20px;
                padding-top: 20px;
                border-top: 1px solid #374151;
                font-family: 'Courier New', monospace;
            }}
            @media only screen and (max-width: 600px) {{
                .content {{
                    padding: 30px 25px;
                }}
                .header {{
                    padding: 40px 25px;
                }}
                .agent-card {{
                    padding: 16px;
                }}
                .cta-section {{
                    padding: 25px 20px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Welcome to Sponte AI</h1>
                <p>Your autonomous local SEO platform</p>
            </div>

            <div class="content">
                <p class="greeting">Hey {business_name}! 👋</p>

                <p class="intro">
                    Thanks for joining Sponte AI! Your account is live and your AI agents are ready to supercharge your local SEO.
                    Here's what we've set up for you:
                </p>

                <div class="section-title">
                    <span class="emoji">🤖</span>
                    <span>Your AI Agent Team</span>
                </div>

                <div class="agent-grid">
                    <div class="agent-card">
                        <div class="agent-card-header">
                            <div class="agent-name">
                                <span class="agent-icon">🗺️</span>
                                <span>GBP Agent</span>
                            </div>
                            <span class="badge">Draft</span>
                        </div>
                        <p class="agent-description">Managing your Google Business Profile with posts, updates, and optimizations</p>
                    </div>

                    <div class="agent-card">
                        <div class="agent-card-header">
                            <div class="agent-name">
                                <span class="agent-icon">📍</span>
                                <span>NAP Agent</span>
                            </div>
                            <span class="badge">Draft</span>
                        </div>
                        <p class="agent-description">Ensuring consistent listings across 50+ directories and platforms</p>
                    </div>

                    <div class="agent-card">
                        <div class="agent-card-header">
                            <div class="agent-name">
                                <span class="agent-icon">🔍</span>
                                <span>Keyword Agent</span>
                            </div>
                            <span class="badge">Draft</span>
                        </div>
                        <p class="agent-description">Researching high-value local search opportunities in your market</p>
                    </div>

                    <div class="agent-card">
                        <div class="agent-card-header">
                            <div class="agent-name">
                                <span class="agent-icon">✍️</span>
                                <span>Blog Agent</span>
                            </div>
                            <span class="badge">Draft</span>
                        </div>
                        <p class="agent-description">Creating SEO-optimized blog content tailored to your audience</p>
                    </div>

                    <div class="agent-card">
                        <div class="agent-card-header">
                            <div class="agent-name">
                                <span class="agent-icon">📱</span>
                                <span>Social Agent</span>
                            </div>
                            <span class="badge">Draft</span>
                        </div>
                        <p class="agent-description">Planning engaging social media posts to boost your online presence</p>
                    </div>

                    <div class="agent-card">
                        <div class="agent-card-header">
                            <div class="agent-name">
                                <span class="agent-icon">📊</span>
                                <span>Reporting Agent</span>
                            </div>
                            <span class="badge">Draft</span>
                        </div>
                        <p class="agent-description">Tracking performance metrics and delivering actionable insights</p>
                    </div>
                </div>

                <div class="cta-section">
                    <h3>Ready to Get Started?</h3>
                    <p>Complete your setup in 5 minutes and activate your agents</p>
                    <a href="http://localhost:3000/dashboard/setup/{user_id}" class="cta-button">
                        Complete Setup →
                    </a>
                </div>

                <div class="section-title">
                    <span class="emoji">✅</span>
                    <span>Next Steps</span>
                </div>

                <div class="steps-list">
                    <ol>
                        <li><strong>Connect Google Business Profile</strong> — Authorize the GBP Agent to manage your listing</li>
                        <li><strong>Link your website</strong> — Enable content publishing and SEO tracking</li>
                        <li><strong>Review agent drafts</strong> — Approve or edit AI-generated content before it goes live</li>
                        <li><strong>Upgrade to Autopilot</strong> (optional) — Let agents publish automatically</li>
                    </ol>
                </div>

                <div class="help-section">
                    <h4>Need Help?</h4>
                    <p>Our team is here to help you succeed.</p>
                    <p>📧 <strong>support@sponteai.com</strong> • We typically respond within 2 hours</p>
                </div>
            </div>

            <div class="footer">
                <div class="footer-logo">Sponte AI</div>
                <div class="footer-tagline">Autonomous Local SEO</div>
                <div class="footer-ids">
                    User: {user_id}<br/>
                    Location: {location_id}
                </div>
            </div>
        </div>
    </body>
    </html>
    """

def get_report_email_html(business_name: str, report_type: str, report_data: dict, report_id: str) -> str:
    """
    Generate HTML for weekly/monthly report email.
    Beautiful, data-rich design showing key metrics and insights.
    """
    metrics = report_data.get('metrics', {})
    agent_activity = report_data.get('agentActivity', {})
    insights = report_data.get('insights', [])
    opportunities = report_data.get('opportunities', [])
    period = report_data.get('period', '')
    
    # Helper function to format metric change
    def format_metric_html(metric_data):
        if not metric_data:
            return ""
        current = metric_data.get('current', 0)
        change = metric_data.get('change', 0)
        is_positive = change >= 0
        arrow = '↑' if is_positive else '↓'
        color = '#10B981' if is_positive else '#EF4444'
        
        return f"""
        <div style="text-align: center;">
            <div style="font-size: 36px; font-weight: 700; color: #1A1D2E; margin-bottom: 8px;">
                {current:,}
            </div>
            <div style="color: {color}; font-weight: 700; font-size: 14px;">
                {arrow} {abs(change):.1f}%
            </div>
        </div>
        """
    
    # Build metrics cards HTML
    metrics_html = ""
    metric_items = [
        ('calls', '📞', 'Calls', metrics.get('calls')),
        ('gbpViews', '👀', 'GBP Views', metrics.get('gbpViews')),
        ('directionRequests', '🧭', 'Directions', metrics.get('directionRequests')),
        ('websiteClicks', '🖱️', 'Website Clicks', metrics.get('websiteClicks')),
    ]
    
    for key, icon, label, metric_data in metric_items:
        if metric_data:
            metrics_html += f"""
            <td style="width: 25%; padding: 20px; background: white; border: 2px solid #e5e7eb; border-radius: 12px;">
                <div style="text-align: center; margin-bottom: 10px; font-size: 32px;">{icon}</div>
                <div style="text-align: center; color: #6B7280; font-size: 12px; font-weight: 700; text-transform: uppercase; margin-bottom: 12px;">
                    {label}
                </div>
                {format_metric_html(metric_data)}
            </td>
            """
    
    # Build insights HTML
    insights_html = ""
    for insight in insights[:4]:  # Show top 4 insights
        insights_html += f"""
        <div style="margin: 12px 0; padding-left: 25px; position: relative;">
            <span style="position: absolute; left: 0; color: #10B981; font-weight: 700;">✓</span>
            <span style="color: #4B5563; font-size: 14px; line-height: 1.6;">{insight}</span>
        </div>
        """
    
    # Build opportunities HTML
    opportunities_html = ""
    for opp in opportunities[:4]:  # Show top 4 opportunities
        opportunities_html += f"""
        <div style="margin: 12px 0; padding-left: 25px; position: relative;">
            <span style="position: absolute; left: 0; color: #FF5810; font-weight: 700;">💡</span>
            <span style="color: #4B5563; font-size: 14px; line-height: 1.6;">{opp}</span>
        </div>
        """
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; line-height: 1.6; color: #1A1D2E; background: linear-gradient(135deg, #f5f7fa 0%, #e8eef3 100%); margin: 0; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 40px rgba(0, 0, 0, 0.12);">
            
            <!-- Header -->
            <div style="background: linear-gradient(135deg, #FF5810 0%, #FF3D00 100%); color: white; padding: 40px; text-align: center;">
                <div style="font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; opacity: 0.9; margin-bottom: 8px;">
                    {report_type.upper()} REPORT
                </div>
                <h1 style="margin: 0 0 8px 0; font-size: 28px; font-weight: 700; letter-spacing: -0.5px;">
                    {business_name}
                </h1>
                <p style="margin: 0; font-size: 15px; opacity: 0.95;">
                    {period}
                </p>
            </div>

            <!-- Content -->
            <div style="padding: 35px;">
                
                <!-- Greeting -->
                <p style="font-size: 16px; color: #4B5563; margin: 0 0 30px 0;">
                    Here's how your business performed this {'week' if report_type == 'weekly' else 'month'}. 
                    Your AI agents have been working hard to grow your local presence! 🚀
                </p>

                <!-- Key Metrics -->
                <h2 style="font-size: 20px; font-weight: 700; color: #1A1D2E; margin: 0 0 20px 0;">
                    📊 Key Metrics
                </h2>
                
                <table cellpadding="0" cellspacing="8" style="width: 100%; margin-bottom: 35px;">
                    <tr>
                        {metrics_html}
                    </tr>
                </table>

                <!-- Reviews (if available) -->
                {f'''
                <div style="background: linear-gradient(135deg, #fff4ed 0%, #ffe8d6 100%); border: 2px solid #FF5810; border-radius: 12px; padding: 25px; margin-bottom: 35px;">
                    <div style="text-align: center;">
                        <div style="font-size: 32px; margin-bottom: 10px;">⭐</div>
                        <div style="font-size: 40px; font-weight: 700; color: #1A1D2E; margin-bottom: 5px;">
                            {metrics.get('reviews', {}).get('avgRating', 0)}
                        </div>
                        <div style="color: #6B7280; font-size: 14px; margin-bottom: 10px;">
                            Average Rating • {metrics.get('reviews', {}).get('count', 0)} reviews
                        </div>
                        <div style="color: #10B981; font-weight: 700; font-size: 16px;">
                            +{metrics.get('reviews', {}).get('newReviews', 0)} new {'this week' if report_type == 'weekly' else 'this month'}
                        </div>
                    </div>
                </div>
                ''' if metrics.get('reviews') else ''}

                <!-- Insights -->
                {f'''
                <h2 style="font-size: 18px; font-weight: 700; color: #1A1D2E; margin: 35px 0 15px 0; display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 24px;">💡</span>
                    <span>Key Insights</span>
                </h2>
                <div style="background: #f9fafb; border: 2px solid #e5e7eb; border-radius: 12px; padding: 20px;">
                    {insights_html}
                </div>
                ''' if insights else ''}

                <!-- Opportunities Identified -->
                {f'''
                <h2 style="font-size: 18px; font-weight: 700; color: #1A1D2E; margin: 25px 0 15px 0; display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 24px;">🔍</span>
                    <span>Opportunities Identified</span>
                </h2>
                <div style="background: #f9fafb; border: 2px solid #e5e7eb; border-radius: 12px; padding: 20px;">
                    {opportunities_html}
                </div>
                ''' if opportunities else ''}

                <!-- CTA Button -->
                <div style="text-align: center; margin: 35px 0 10px 0;">
                    <a href="http://localhost:3000/dashboard/reports/{report_id}" 
                       style="display: inline-block; background: linear-gradient(135deg, #FF5810 0%, #FF3D00 100%); color: white; padding: 16px 40px; text-decoration: none; border-radius: 10px; font-weight: 700; font-size: 16px; box-shadow: 0 4px 15px rgba(255, 88, 16, 0.3);">
                        View Full Report →
                    </a>
                </div>

                <!-- Footer Note -->
                <div style="margin-top: 35px; padding-top: 25px; border-top: 2px solid #e5e7eb; text-align: center;">
                    <p style="margin: 0; color: #6B7280; font-size: 13px; line-height: 1.6;">
                        Your AI agents are working 24/7 to improve your local SEO.<br/>
                        <a href="http://localhost:3000/dashboard" style="color: #FF5810; text-decoration: none; font-weight: 600;">Visit Dashboard</a> to manage your agents.
                    </p>
                </div>
            </div>

            <!-- Footer -->
            <div style="background: linear-gradient(135deg, #1A1D2E 0%, #2d3748 100%); padding: 30px; text-align: center; color: #9CA3AF;">
                <div style="font-size: 20px; font-weight: 800; color: white; margin-bottom: 6px;">
                    Sponte AI
                </div>
                <div style="font-size: 12px; color: #9CA3AF;">
                    Autonomous Local SEO • Every Monday
                </div>
            </div>
        </div>
    </body>
    </html>
    """
