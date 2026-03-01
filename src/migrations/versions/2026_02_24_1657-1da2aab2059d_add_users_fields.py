"""Add users fields

Revision ID: 1da2aab2059d
Revises: fb894fca0730
Create Date: 2026-02-24 16:57:30.944095

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1da2aab2059d'
down_revision: Union[str, Sequence[str], None] = 'fb894fca0730'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.alter_column('users', 'first_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('users', 'last_name',
               existing_type=sa.VARCHAR(),
               nullable=True)



def downgrade() -> None:
    """Downgrade schema."""

    op.alter_column('users', 'last_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('users', 'first_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
