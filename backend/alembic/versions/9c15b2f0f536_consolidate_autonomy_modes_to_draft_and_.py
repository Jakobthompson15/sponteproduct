"""consolidate_autonomy_modes_to_draft_and_autopilot

Revision ID: 9c15b2f0f536
Revises: 84544e62248c
Create Date: 2025-11-19 13:13:40.845388

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c15b2f0f536'
down_revision = '84544e62248c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Consolidate autonomy modes from 3 to 2:
    - Convert 'approve' → 'draft' (both require human interaction)
    - Convert 'auto' → 'autopilot' (legacy naming)
    - Keep 'draft' and 'autopilot' as-is

    Since the enum type needs to be modified, we'll:
    1. Create a temporary column
    2. Migrate data
    3. Drop old column
    4. Rename new column
    5. Recreate enum type with only 2 values
    """
    # Add a temporary text column
    op.add_column('agent_configs', sa.Column('autonomy_mode_new', sa.Text(), nullable=True))

    # Migrate data with conversions (use LOWER to handle both cases)
    op.execute("""
        UPDATE agent_configs
        SET autonomy_mode_new = CASE
            WHEN LOWER(autonomy_mode::text) IN ('approve', 'draft') THEN 'draft'
            WHEN LOWER(autonomy_mode::text) IN ('auto', 'autopilot') THEN 'autopilot'
            ELSE LOWER(autonomy_mode::text)
        END
    """)

    # Drop the old column
    op.drop_column('agent_configs', 'autonomy_mode')

    # Recreate the enum type with only 2 values
    op.execute("DROP TYPE IF EXISTS autonomymode CASCADE")
    op.execute("CREATE TYPE autonomymode AS ENUM ('draft', 'autopilot')")

    # Add back the column with the new enum type
    op.add_column('agent_configs',
                  sa.Column('autonomy_mode', sa.Enum('draft', 'autopilot', name='autonomymode'), nullable=False, server_default='draft'))

    # Copy data from temporary column
    op.execute("""
        UPDATE agent_configs
        SET autonomy_mode = autonomy_mode_new::autonomymode
    """)

    # Drop temporary column
    op.drop_column('agent_configs', 'autonomy_mode_new')


def downgrade() -> None:
    """
    Downgrade is not needed - we can't reliably reverse the consolidation.
    If needed, all records will default to 'draft' mode.
    """
    pass
