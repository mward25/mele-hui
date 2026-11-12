from db import Song
from db.session import SessionLocal
from PySide6.QtCore import Property, QObject, QUrl, Signal, Slot
from PySide6.QtQml import QmlElement

QML_IMPORT_NAME = "MeleHui"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class SongView(QObject):
    songChanged = Signal()
    songIdChanged = Signal()

    def _get_song(self):
        if self._song_id is None:
            return None
        else:
            assert self._song is not None
            return {
                "id": self._song.id,
                "name": self._song.name,
            }

    def _get_pages(self):
        if self._song_id is None:
            return None
        else:
            assert self._song is not None
            assert self._pages is not None
            return self._pages

    def _get_song_id(self):
        return self._song_id

    def _set_song_id(self, song_id):
        self._song_id = song_id
        self.songIdChanged.emit()
        self.reload()

    song = Property(dict, _get_song, notify=songChanged)
    pages = Property(list, _get_pages, notify=songChanged)
    songId = Property(int, _get_song_id, _set_song_id, notify=songIdChanged)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._song_id = None
        self._song = None
        self._pages = None
        self.refresh()

    def refresh(self):
        if self._song_id is None:
            self._song = None
        else:
            session = SessionLocal()
            try:
                self._song = session.get(Song, self._song_id)
                self._pages = []
                for page in self._song.pages:
                    self._pages.append(
                        {
                            "id": page.id,
                            "song_id": page.song_id,
                            "file_path": QUrl.fromLocalFile(page.file_store.full_path),
                        }
                    )
                self.songChanged.emit()
            finally:
                session.close()

    @Slot()
    def reload(self):
        self.refresh()
