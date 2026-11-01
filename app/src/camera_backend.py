"""Python camera capture backend wired from camera.qml."""

import os
import uuid
from pathlib import Path

from PySide6.QtCore import QObject, Slot, QBuffer, QIODevice, QByteArray
from PySide6.QtGui import QImage

from db import FileStore
from db.session import SessionLocal
from db.events import STORAGE_ROOT


class CameraBackend(QObject):
    @Slot(QImage, result=str)
    def imageToDataUrl(self, image: QImage) -> str:
        buffer = QBuffer()
        buffer.open(QIODevice.OpenModeFlag.WriteOnly)
        image.save(buffer, "PNG")
        encoded = buffer.data().toBase64().data().decode("ascii")
        buffer.close()
        return "data:image/png;base64," + encoded

    @Slot(QImage, result=int)
    def saveCapture(self, image: QImage) -> int:
        session = SessionLocal()
        try:
            fs = FileStore(bucket="captures", filename=f"{uuid.uuid4()}.png")
            session.add(fs)
            session.flush()  # populate fs.id
            print(f"Python ID: {fs.id}")
            return_val = fs.id

            out_path = fs.full_path
            out_path.parent.mkdir(parents=True, exist_ok=True)

            if not image.save(str(out_path)):
                raise RuntimeError(f"failed to save image to {out_path}")

            session.commit()
            return fs.id
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
