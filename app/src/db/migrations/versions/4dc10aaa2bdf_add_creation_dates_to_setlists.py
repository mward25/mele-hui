"""Add creation dates to setlists

Revision ID: 4dc10aaa2bdf
Revises: c2d3e4f5a6b7
Create Date: 2026-11-16 14:01:00.835750

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4dc10aaa2bdf"
down_revision: Union[str, Sequence[str], None] = "c2d3e4f5a6b7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("PRAGMA foreign_keys=OFF")
    op.create_table(
        "setlist_new",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("creation_date", sa.DateTime(), nullable=False, server_default=sa.sql.func.now()),
    )
    op.execute("INSERT INTO setlist_new(id, name) SELECT id, name FROM setlist")
    op.drop_table("setlist")
    op.execute("ALTER TABLE setlist_new RENAME TO setlist")
    op.execute("PRAGMA foreign_keys=ON")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("setlist", "creation_date")
