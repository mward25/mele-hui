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
    needsPracticeChanged = Signal()

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

    def _set_needs_practice(self, needs_practice):
        session = SessionLocal()
        try:
            session.query(Song).filter(Song.id == self._song_id).update({"needs_practice": needs_practice})
            session.commit()
        finally:
            session.close()
        self.refresh()

    def _get_needs_practice(self):
        if self._song is None:
            return False
        return self._song.needs_practice

    song = Property(dict, _get_song, notify=songChanged)
    pages = Property(list, _get_pages, notify=songChanged)
    songId = Property(int, _get_song_id, _set_song_id, notify=songIdChanged)
    needsPractice = Property(bool, _get_needs_practice, _set_needs_practice, notify=needsPracticeChanged)

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
                self.needsPracticeChanged.emit()
                self.songChanged.emit()
            finally:
                session.close()

    @Slot()
    def reload(self):
        self.refresh()
