"""create hosts table

Revision ID: 8eea77e587f0
Revises: 9249fb305ef1
Create Date: 2026-08-21 06:49:01.450082

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8eea77e587f0"
down_revision: Union[str, Sequence[str], None] = "9249fb305ef1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create hosts table."""

    op.create_table(
        "hosts",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "hostname",
            sa.String(length=100),
            nullable=False,
        ),

        sa.Column(
            "ip_address",
            sa.String(length=45),
            nullable=False,
        ),

        sa.Column(
            "mac_address",
            sa.String(length=17),
            nullable=False,
        ),

        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
        ),

        sa.Column(
            "risk_score",
            sa.Float(),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
        ),

        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("hostname"),
        sa.UniqueConstraint("ip_address"),
        sa.UniqueConstraint("mac_address"),
    )

    op.create_index(
        "ix_hosts_id",
        "hosts",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    """Drop hosts table."""

    op.drop_index(
        "ix_hosts_id",
        table_name="hosts",
    )

    op.drop_table("hosts")