"""Add facilities

Revision ID: c0dc0ea68097
Revises: 1477aa9c82ed
Create Date: 2026-03-03 23:27:37.685783

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c0dc0ea68097"
down_revision: Union[str, Sequence[str], None] = "1477aa9c82ed"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "facilities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "rooms_facilities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("rooms_id", sa.Integer(), nullable=False),
        sa.Column("facilities_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["facilities_id"],
            ["facilities.id"],
        ),
        sa.ForeignKeyConstraint(
            ["rooms_id"],
            ["rooms.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    

def downgrade() -> None:
  

    op.drop_table("rooms_facilities")
    op.drop_table("facilities")
