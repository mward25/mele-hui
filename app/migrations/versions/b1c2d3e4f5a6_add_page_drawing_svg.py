"""add page drawing_svg

Revision ID: b1c2d3e4f5a6
Revises: 49a50b12f4a3
Create Date: 2026-11-01

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "b1c2d3e4f5a6"
down_revision: Union[str, Sequence[str], None] = "9d9fb8487966"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("page", sa.Column("drawing_svg", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("page", "drawing_svg")
