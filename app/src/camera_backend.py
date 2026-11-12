"""Python camera capture backend wired from camera.qml."""

import uuid

import pymupdf as fitz
from db import FileStore
from db.session import SessionLocal
from PySide6.QtCore import QBuffer, QIODevice, QObject, QUrl, Slot
from PySide6.QtGui import QImage, QTransform


class CameraBackend(QObject):
    @Slot(QUrl, result="QVariantList")
    def pdfToImages(self, source: QUrl) -> list[QImage]:
        images = []
        doc = fitz.open(source.toLocalFile())
        try:
            for page in doc:
                print("Adding page")
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                qimg = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888)
                images.append(qimg.copy())
        finally:
            doc.close()
        return images

    @Slot(QImage, int, result=QImage)
    def rotateImage(self, image: QImage, degrees: int) -> QImage:
        if image is None or image.isNull():
            return image
        return image.transformed(QTransform().rotate(degrees))

    @Slot(QUrl, result=QImage)
    def loadImage(self, source: QUrl) -> QImage:
        return QImage(source.toLocalFile())

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
