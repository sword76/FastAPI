"""Remove facilities

Revision ID: 169398de005e
Revises: c0dc0ea68097
Create Date: 2026-03-04 14:27:25.587939

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "169398de005e"
down_revision: Union[str, Sequence[str], None] = "c0dc0ea68097"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    op.add_column(
        "rooms_facilities", sa.Column("room_id", sa.Integer(), nullable=False)
    )
    op.add_column(
        "rooms_facilities", sa.Column("facility_id", sa.Integer(), nullable=False)
    )
    op.drop_constraint(
        op.f("rooms_facilities_facilities_id_fkey"),
        "rooms_facilities",
        type_="foreignkey",
    )
    op.drop_constraint(
        op.f("rooms_facilities_rooms_id_fkey"), "rooms_facilities", type_="foreignkey"
    )
    op.create_foreign_key(
        None, "rooms_facilities", "facilities", ["facility_id"], ["id"]
    )
    op.create_foreign_key(None, "rooms_facilities", "rooms", ["room_id"], ["id"])
    op.drop_column("rooms_facilities", "rooms_id")
    op.drop_column("rooms_facilities", "facilities_id")


def downgrade() -> None:
    """Downgrade schema."""
  
    op.add_column(
        "rooms_facilities",
        sa.Column("facilities_id", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "rooms_facilities",
        sa.Column("rooms_id", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.drop_constraint(None, "rooms_facilities", type_="foreignkey")
    op.drop_constraint(None, "rooms_facilities", type_="foreignkey")
    op.create_foreign_key(
        op.f("rooms_facilities_rooms_id_fkey"),
        "rooms_facilities",
        "rooms",
        ["rooms_id"],
        ["id"],
    )
    op.create_foreign_key(
        op.f("rooms_facilities_facilities_id_fkey"),
        "rooms_facilities",
        "facilities",
        ["facilities_id"],
        ["id"],
    )
    op.drop_column("rooms_facilities", "facility_id")
    op.drop_column("rooms_facilities", "room_id")
