"""Initial migration

Revision ID: 3f6e9714d5f7
Revises: 15fa3dbb94b3
Create Date: 2026-02-05 09:53:36.437600

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f6e9714d5f7'
down_revision: Union[str, Sequence[str], None] = '15fa3dbb94b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table('hotels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('location', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )



def downgrade() -> None:

    op.drop_table('hotels')

