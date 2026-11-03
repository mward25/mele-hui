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
                        self._songs.append({"id": song.id, "name": song.name})
            finally:
                session.close()
        self.endResetModel()
        self.songsChanged.emit()

    @Slot()
    def reload(self):
        self.refresh()
