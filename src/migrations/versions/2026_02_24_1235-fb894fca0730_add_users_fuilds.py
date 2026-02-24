"""Add users fuilds

Revision ID: fb894fca0730
Revises: f5a03961fabe
Create Date: 2026-02-24 12:35:37.777678

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fb894fca0730'
down_revision: Union[str, Sequence[str], None] = 'f5a03961fabe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('first_name', sa.String(), nullable=False))
    op.add_column('users', sa.Column('last_name', sa.String(), nullable=False))
    op.add_column('users', sa.Column('hashed_password', sa.String(length=200), nullable=False))
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=False))
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=False))
    op.add_column('users', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('users', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.drop_column('users', 'password')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('users', sa.Column('password', sa.VARCHAR(length=200), autoincrement=False, nullable=False))
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_column('users', 'updated_at')
    op.drop_column('users', 'created_at')
    op.drop_column('users', 'is_admin')
    op.drop_column('users', 'is_active')
    op.drop_column('users', 'hashed_password')
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'first_name')
