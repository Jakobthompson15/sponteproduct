"""
Database verification script.
Run this after setting up to verify all tables and data.

Usage:
    python verify_db.py
"""

from app.database import SessionLocal
from app.models import User, Location, AgentConfig, OAuthToken, Task
from sqlalchemy import inspect


def verify_database():
    """Verify database setup and show current data."""

    print("\n" + "="*60)
    print("SPONTE AI - DATABASE VERIFICATION")
    print("="*60 + "\n")

    db = SessionLocal()

    try:
        # Check database connection
        print("✅ Database connection successful")

        # Verify tables exist
        inspector = inspect(db.bind)
        tables = inspector.get_table_names()
        print(f"\n📊 Tables found: {len(tables)}")
        for table in sorted(tables):
            print(f"   - {table}")

        # Count records in each table
        users = db.query(User).all()
        locations = db.query(Location).all()
        agents = db.query(AgentConfig).all()
        tokens = db.query(OAuthToken).all()
        tasks = db.query(Task).all()

        print(f"\n📈 Data Summary:")
        print(f"   Users:        {len(users)}")
        print(f"   Locations:    {len(locations)}")
        print(f"   Agent Configs: {len(agents)}")
        print(f"   OAuth Tokens: {len(tokens)}")
        print(f"   Tasks:        {len(tasks)}")

        # Show user details
        if users:
            print(f"\n👥 USERS ({len(users)}):")
            for user in users:
                print(f"   - {user.email}")
                print(f"     ID: {user.id}")
                print(f"     Tier: {user.subscription_tier}")
                print(f"     Onboarding: {'✅ Complete' if user.onboarding_completed else '❌ Incomplete'}")
                print(f"     Locations: {len(user.locations)}")
                print()

        # Show location details
        if locations:
            print(f"\n📍 LOCATIONS ({len(locations)}):")
            for loc in locations:
                print(f"   - {loc.business_name}")
                if loc.dba_name:
                    print(f"     DBA: {loc.dba_name}")
                print(f"     Address: {loc.street_address}, {loc.city}, {loc.state} {loc.zip_code}")
                print(f"     Phone: {loc.phone_primary}")
                print(f"     Category: {loc.primary_category}")
                print(f"     Website: {loc.website_url or 'Not set'}")
                print(f"     CMS: {loc.cms_platform or 'Not set'}")
                print(f"     Agents: {len(loc.agent_configs)}")
                print()

        # Show agent configurations
        if agents:
            print(f"\n🤖 AGENT CONFIGURATIONS ({len(agents)}):")
            agent_summary = {}
            for agent in agents:
                agent_type = agent.agent_type.value
                if agent_type not in agent_summary:
                    agent_summary[agent_type] = 0
                agent_summary[agent_type] += 1

            for agent_type, count in sorted(agent_summary.items()):
                print(f"   - {agent_type.upper()}: {count} configured")

            print(f"\n   Agent Details:")
            for agent in agents[:6]:  # Show first 6 agents
                print(f"   - {agent.agent_type.value.upper()}")
                print(f"     Mode: {agent.autonomy_mode.value}")
                print(f"     Active: {'✅' if agent.is_active else '❌'}")

        # Show OAuth tokens (without revealing actual tokens)
        if tokens:
            print(f"\n🔐 OAUTH TOKENS ({len(tokens)}):")
            for token in tokens:
                print(f"   - {token.provider.value}")
                print(f"     User: {token.user_id}")
                print(f"     Expires: {token.expires_at}")
                print()

        # Show tasks
        if tasks:
            print(f"\n📋 TASKS ({len(tasks)}):")
            task_summary = {}
            for task in tasks:
                status = task.status.value
                if status not in task_summary:
                    task_summary[status] = 0
                task_summary[status] += 1

            for status, count in sorted(task_summary.items()):
                print(f"   - {status.upper()}: {count}")

        print("\n" + "="*60)
        print("✅ Database verification complete!")
        print("="*60 + "\n")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}\n")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    verify_database()
