from PySide6.QtCore import QObject, Signal, Property, Slot, QUrl
from PySide6.QtQml import QmlElement

from db import Song
from db.session import SessionLocal

QML_IMPORT_NAME = "MeleHui"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class SongGalleryList(QObject):
    songsChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._songs = []
        self.refresh()

    def _get_songs(self):
        return list(self._songs)

    songs = Property("QVariantList", _get_songs, notify=songsChanged)

    def get_first_page_or_nil(self, s):
        first_page = s.pages
        if len(s.pages) > 0:
            first_page = QUrl.fromLocalFile(s.pages[0].file_store.full_path)
        else:
            first_page = None
        return first_page

    def refresh(self):
        session = SessionLocal()
        try:
            rows = session.query(Song).all()
            self._songs = [
                {
                    "id": s.id,
                    "name": s.name,
                    "pageCount": len(s.pages),
                    "first_page_img_path": self.get_first_page_or_nil(s),
                }
                for s in rows
            ]
            self.songsChanged.emit()
        finally:
            session.close()

    @Slot()
    def reload(self):
        self.refresh()
