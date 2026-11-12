"""initial schema

Revision ID: 9d9fb8487966
Revises:
Create Date: 2026-11-01 10:31:42.535633

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "9d9fb8487966"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "song",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(), nullable=True),
    )
    op.create_table(
        "file_store",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("bucket", sa.String(), nullable=True, server_default="captures"),
        sa.Column("filename", sa.String(), nullable=False),
    )
    op.create_table(
        "setlist",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(), nullable=True),
    )
    op.create_table(
        "page",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("song_id", sa.Integer(), sa.ForeignKey("song.id"), nullable=False),
        sa.Column(
            "file_id", sa.Integer(), sa.ForeignKey("file_store.id"), nullable=False
        ),
    )
    op.create_table(
        "setlist_song",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "setlist_id", sa.Integer(), sa.ForeignKey("setlist.id"), nullable=False
        ),
        sa.Column("song_id", sa.Integer(), sa.ForeignKey("song.id"), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("setlist_song")
    op.drop_table("page")
    op.drop_table("setlist")
    op.drop_table("file_store")
    op.drop_table("song")
