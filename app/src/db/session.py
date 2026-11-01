import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .base import Base

DATABASE_URL = os.environ.get("MELEHUI_DB_URL", "sqlite:///" + str(Path(__file__).resolve().parents[2] / "melehui.db"))
engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

# Ensure tables exist for dev convenience; Alembic remains source of truth.
Base.metadata.create_all(engine)


def init_db():
    Base.metadata.create_all(engine)
