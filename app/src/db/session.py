import os
from pathlib import Path

from PySide6.QtCore import QCoreApplication, QStandardPaths
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .base import Base


def _data_dir() -> Path:
    try:
        base = QStandardPaths.writableLocation(QStandardPaths.AppLocalDataLocation)
    except Exception:
        base = ""
    if not base:
        base = str(Path.home() / ".local" / "share" / "melehui")
    p = Path(base)
    p.mkdir(parents=True, exist_ok=True)
    return p


DATABASE_URL = os.environ.get(
    "MELEHUI_DB_URL",
    "sqlite:///" + str(_data_dir() / "melehui.db"),
)
from sqlalchemy import event

engine = create_engine(
    DATABASE_URL, future=True, connect_args={"check_same_thread": False}
)


@event.listens_for(engine, "connect")
def _enable_sqlite_fk(dbapi_conn, _):
    if DATABASE_URL.startswith("sqlite"):
        dbapi_conn.execute("PRAGMA foreign_keys=ON")


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
