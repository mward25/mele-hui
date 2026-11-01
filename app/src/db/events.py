"""SQLAlchemy session hooks for FileStore file cleanup."""

import os
from pathlib import Path

from sqlalchemy import event
from sqlalchemy.orm import Session

from .file_store import FileStore

STORAGE_ROOT = Path(os.environ.get("MELEHUI_STORAGE_ROOT", "storage")).resolve()

_pending_deletions: list[Path] = []


@event.listens_for(Session, "before_flush")
def collect_deleted_file_paths(session, flush_context, instances):
    for obj in list(session.deleted):
        if isinstance(obj, FileStore):
            _pending_deletions.append(obj.full_path)


@event.listens_for(Session, "after_commit")
def delete_files_after_commit(session):
    for file_path in _pending_deletions:
        try:
            if file_path.is_file():
                file_path.unlink()
        except OSError:
            pass
    _pending_deletions.clear()


@event.listens_for(Session, "after_rollback")
def clear_pending_deletions_on_rollback(session):
    _pending_deletions.clear()
