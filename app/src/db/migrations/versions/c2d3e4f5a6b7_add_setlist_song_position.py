"""add setlist_song position

Revision ID: c2d3e4f5a6b7
Revises: b1c2d3e4f5a6
Create Date: 2026-11-03
"""

from alembic import op
import sqlalchemy as sa

revision = "c2d3e4f5a6b7"
down_revision = "b1c2d3e4f5a6"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "setlist_song",
        sa.Column("position", sa.Integer(), nullable=False, server_default="0"),
    )
    # backfill
    conn = op.get_bind()
    rows = conn.execute(
        sa.text("SELECT id, setlist_id FROM setlist_song ORDER BY id")
    ).fetchall()
    counters = {}
    for rid, sid in rows:
        counters[sid] = counters.get(sid, 0)
        conn.execute(
            sa.text("UPDATE setlist_song SET position=:p WHERE id=:i"),
            {"p": counters[sid], "i": rid},
        )
        counters[sid] += 1


def downgrade():
    op.drop_column("setlist_song", "position")
