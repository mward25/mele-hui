from PySide6.QtCore import (
    QAbstractListModel,
    Qt,
    Signal,
    Property,
    Slot,
    QUrl,
    QModelIndex,
)
from PySide6.QtQml import QmlElement

from db import Setlist, SetlistSong, Song
from db.session import SessionLocal

QML_IMPORT_NAME = "MeleHui"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class SetlistView(QAbstractListModel):
    setlistIdChanged = Signal()
    songsChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setlist_id = None
        self._songs = []
        self._roles = {
            Qt.UserRole + 1: b"id",
            Qt.UserRole + 2: b"name",
            Qt.UserRole + 3: b"setlistSongId",
        }

    def _get_setlist_id(self):
        return self._setlist_id

    def _set_setlist_id(self, value):
        self._setlist_id = value
        self.setlistIdChanged.emit()
        self.reload()

    setlistId = Property("int", _get_setlist_id, _set_setlist_id, notify=setlistIdChanged)

    def rowCount(self, parent=QModelIndex()):
        return len(self._songs)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self._songs):
            return None
        song = self._songs[index.row()]
        if role == Qt.UserRole + 1:
            return song.get("id")
        if role == Qt.UserRole + 2:
            return song.get("name")
        if role == Qt.UserRole + 3:
            return song.get("setlistSongId")
        return None

    def roleNames(self):
        return self._roles

    def refresh(self):
        self.beginResetModel()
        self._songs = []
        if self._setlist_id is not None:
            session = SessionLocal()
            try:
                setlist = session.get(Setlist, self._setlist_id)
                if setlist is not None:
                    for ss in setlist.setlist_songs:
                        song = ss.song
                        self._songs.append({"id": song.id, "name": song.name, "setlistSongId": ss.id})
            finally:
                session.close()
        self.endResetModel()
        self.songsChanged.emit()

    @Slot(int)
    def addSong(self, song_id: int) -> None:
        if self._setlist_id is None:
            return
        session = SessionLocal()
        try:
            assert song_id is not None
            assert self._setlist_id is not None
            existing = session.query(SetlistSong).filter_by(setlist_id=self._setlist_id).count()
            session.add(SetlistSong(setlist_id=self._setlist_id, song_id=int(song_id), position=existing))
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
        self.refresh()

    @Slot(int, int)
    def moveSong(self, fromIndex: int, toIndex: int) -> None:
        if self._setlist_id is None:
            return
        if fromIndex < 0 or toIndex < 0 or fromIndex >= len(self._songs) or toIndex >= len(self._songs):
            return
        if fromIndex == toIndex:
            return
        session = SessionLocal()
        try:
            setlist = session.get(Setlist, self._setlist_id)
            if setlist is None:
                return
            items = list(setlist.setlist_songs)
            item = items.pop(fromIndex)
            items.insert(toIndex, item)
            for idx, ss in enumerate(items):
                ss.position = idx
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
        self.refresh()

    @Slot()
    def reload(self):
        self.refresh()
