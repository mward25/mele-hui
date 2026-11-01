from PySide6.QtCore import QObject, Slot, Signal, Property
from PySide6.QtQml import QmlElement

from db import Song, Page
from db.session import SessionLocal


QML_IMPORT_NAME = "MeleHui"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class SongBackend(QObject):
    pagesChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._pages: list[int] = []

    def _get_pages(self):
        return list(self._pages)

    pages = Property("QVariantList", _get_pages, notify=pagesChanged)

    @Slot(int)
    def addPage(self, page_id: int) -> None:
        if page_id not in self._pages:
            self._pages.append(page_id)
            self.pagesChanged.emit()

    @Slot()
    def clear(self) -> None:
        self._pages.clear()
        self.pagesChanged.emit()

    @Slot(str, "QVariantList", result=int)
    def createSong(self, name: str, file_ids) -> int:
        name = (name or "").strip()
        if not name:
            return -1
        session = SessionLocal()
        try:
            song = Song(name=name)
            session.add(song)
            session.flush()
            for file_id in file_ids or []:
                session.add(Page(song_id=song.id, file_id=int(file_id)))
            session.commit()
            return song.id
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
