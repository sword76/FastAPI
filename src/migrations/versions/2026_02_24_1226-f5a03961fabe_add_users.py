"""Add users

Revision ID: f5a03961fabe
Revises: 5b41f1b2b33b
Create Date: 2026-02-24 12:26:42.000007

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f5a03961fabe'
down_revision: Union[str, Sequence[str], None] = '5b41f1b2b33b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=200), nullable=False),
    sa.Column('password', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    


def downgrade() -> None:
    """Downgrade schema."""
   
    op.drop_table('users')
    
