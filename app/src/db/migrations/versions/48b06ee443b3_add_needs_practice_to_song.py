"""add_needs_practice_to_song

Revision ID: 48b06ee443b3
Revises: 4dc10aaa2bdf
Create Date: 2026-11-16 14:39:55.800469

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "48b06ee443b3"
down_revision: Union[str, Sequence[str], None] = "4dc10aaa2bdf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("song", sa.Column("needs_practice", sa.Boolean(), nullable=False, server_default="FALSE"))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("song", "needs_practice")
