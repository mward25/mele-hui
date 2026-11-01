"""AutoCropper: QML element that crops an input QImage and exposes croppedImage."""

from PySide6.QtCore import QObject, Signal, Property
from PySide6.QtGui import QImage
from PySide6.QtQml import QmlElement

QML_IMPORT_NAME = "MeleHui"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class AutoCropper(QObject):
    imageChanged = Signal()
    croppedImageChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._image = QImage()
        self._cropped = QImage()

    def _get_image(self):
        return self._image

    def _set_image(self, value):
        if value == self._image:
            return
        self._image = value if isinstance(value, QImage) else QImage(value)
        self.imageChanged.emit()
        self._recompute()

    image = Property(QImage, _get_image, _set_image, notify=imageChanged)

    def _get_cropped(self):
        return self._cropped

    croppedImage = Property(QImage, _get_cropped, notify=croppedImageChanged)

    def _recompute(self):
        if self._image.isNull():
            self._cropped = QImage()
            self.croppedImageChanged.emit()
            return
        try:
            import cv2
            import numpy as np
        except Exception:
            # OpenCV not available; pass through unchanged.
            self._cropped = self._image.copy()
            self.croppedImageChanged.emit()
            return

        qimg = self._image.convertToFormat(QImage.Format.Format_RGB888)
        h, w = qimg.height(), qimg.width()
        bpl = qimg.bytesPerLine()
        arr = np.frombuffer(qimg.constBits(), dtype=np.uint8).reshape((h, bpl))[:, : w * 3].reshape((h, w, 3))
        bgr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            self._cropped = self._image.copy()
            self.croppedImageChanged.emit()
            return
        largest = max(contours, key=cv2.contourArea)
        x, y, cw, ch = cv2.boundingRect(largest)
        # Pad a bit
        pad = 8
        x0 = max(0, x - pad)
        y0 = max(0, y - pad)
        x1 = min(w, x + cw + pad)
        y1 = min(h, y + ch + pad)
        cropped_bgr = bgr[y0:y1, x0:x1]
        rgb = cv2.cvtColor(cropped_bgr, cv2.COLOR_BGR2RGB)
        ch_, cw_, _ = rgb.shape
        out = QImage(rgb.data, cw_, ch_, cw_ * 3, QImage.Format.Format_RGB888).copy()
        self._cropped = out
        self.croppedImageChanged.emit()
