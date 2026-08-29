"""link alerts to hosts

Revision ID: c655599013a5
Revises: 8eea77e587f0
Create Date: 2026-08-21 07:03:37.890105
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c655599013a5"
down_revision: Union[str, Sequence[str], None] = "8eea77e587f0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "alerts",
        sa.Column(
            "host_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.create_foreign_key(
        "fk_alerts_host_id",
        "alerts",
        "hosts",
        ["host_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_alerts_host_id",
        "alerts",
        type_="foreignkey",
    )

    op.drop_column(
        "alerts",
        "host_id",
    )