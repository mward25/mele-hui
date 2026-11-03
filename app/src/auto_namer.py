"""AutoNamer: QML element that returns the calculated name of a
piece of paper.."""

from PySide6.QtCore import QObject, Signal, Property
from PySide6.QtGui import QImage
from PySide6.QtQml import QmlElement

from PIL import Image
import pyocr

import cv2
import numpy as np

QML_IMPORT_NAME = "MeleHui"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class AutoNamer(QObject):
    imageChanged = Signal()
    titleChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._image = QImage()
        self._title = ""

    def _get_image(self):
        return self._image

    def _set_image(self, value):
        if value == self._image:
            return
        self._image = value if isinstance(value, QImage) else QImage(value)
        self.imageChanged.emit()
        self._recompute()

    image = Property(QImage, _get_image, _set_image, notify=imageChanged)

    def _get_title(self):
        return self._title

    title = Property(str, _get_title, notify=titleChanged)

    def _recompute(self):
        print("Computing title")
        if self._image.isNull():
            self.titleChanged.emit()
            return

        tools = pyocr.get_available_tools()
        tool = tools[0]

        qimg = self._image.convertToFormat(QImage.Format.Format_RGB888)
        h, w = qimg.height(), qimg.width()
        bpl = qimg.bytesPerLine()
        # Image as array for cv2
        arr = (
            np.frombuffer(qimg.constBits(), dtype=np.uint8)
            .reshape((h, bpl))[:, : w * 3]
            .reshape((h, w, 3))
        )
        # Extract to pillow format
        pill_img = Image.fromarray(arr)
        print(f"Setting title")
        self._title = tool.image_to_string(
            pill_img,
            # @TODO Other languages.
            lang="eng",
            builder=pyocr.builders.TextBuilder(),
        ).split("\n")[0]
        print(f'Title: "{self._title}"')
        self.titleChanged.emit()
