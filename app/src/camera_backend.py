"""Python camera capture backend wired from camera.qml."""

import os
import uuid
from pathlib import Path

from PySide6.QtCore import QObject, Slot
from PySide6.QtGui import QImage

from db import FileStore
from db.session import SessionLocal
from db.events import STORAGE_ROOT


class CameraBackend(QObject):
    @Slot(QImage)
    def saveCapture(self, image: QImage) -> str:
        session = SessionLocal()
        try:
            fs = FileStore(bucket="captures", filename=f"{uuid.uuid4()}.png")
            session.add(fs)
            session.flush()  # populate fs.id

            out_path = fs.full_path
            out_path.parent.mkdir(parents=True, exist_ok=True)

            if not image.save(str(out_path)):
                raise RuntimeError(f"failed to save image to {out_path}")

            session.commit()
            return str(out_path)
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
