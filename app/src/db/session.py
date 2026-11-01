import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .base import Base

DATABASE_URL = os.environ.get("MELEHUI_DB_URL", "sqlite:///" + str(Path(__file__).resolve().parents[2] / "melehui.db"))
engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def init_db():
    # Run Alembic migrations to bring schema up to date.
    from alembic.config import Config
    from alembic import command as alembic_command
    import os
    app_root = Path(__file__).resolve().parents[2]
    cfg = Config(str(app_root / "alembic.ini"))
    cfg.set_main_option("script_location", str(app_root / "migrations"))
    cfg.set_main_option("sqlalchemy.url", DATABASE_URL)
    alembic_command.upgrade(cfg, "head")
