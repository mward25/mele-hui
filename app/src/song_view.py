from PySide6.QtCore import QObject, Signal, Property, Slot, QUrl
from PySide6.QtQml import QmlElement

from db import Song
from db.session import SessionLocal

QML_IMPORT_NAME = "MeleHui"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
class SongView(QObject):
    songChanged = Signal()
    songIdChanged = Signal()

    def _get_song(self):
        if self._song_id == None:
            return None
        else:
            assert(self._song != None)
            return {
                "id": self._song.id,
                "name": self._song.name,
            }
    def _get_pages(self):
        if self._song_id == None:
            return None
        else:
            assert(self._song != None)
            assert(self._pages != None)
            return self._pages

    def _get_song_id(self):
        return self._song_id
    def _set_song_id(self, song_id):
        self._song_id = song_id
        self.songIdChanged.emit()
        self.reload()
    song = Property("QVariantMap", _get_song, notify=songChanged)
    pages = Property("QVariantList", _get_pages, notify=songChanged)
    songId = Property("int", _get_song_id, _set_song_id, notify=songIdChanged)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._song_id = None
        self._song = None
        self._pages = None
        self.refresh()

    # @Slot(int, result=int)
    # def songId(self, id):
    #     self._song_id = id
    #     self.refresh()
    #     return self._song_id

    def refresh(self):
        if self._song_id == None:
            self._song = None
        else:
            session = SessionLocal()
            try:
                self._song = session.get(Song, self._song_id)
                self._pages = []
                for page in self._song.pages:
                    self._pages.append({"id": page.id, "song_id": page.song_id, "file_path": QUrl.fromLocalFile(page.file_store.full_path)})
                self.songChanged.emit()
            finally:
                session.close()
    @Slot()
    def reload(self):
        self.refresh()
