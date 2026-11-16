from db import Setlist
from db.session import SessionLocal
from PySide6.QtCore import Property, QObject, QUrl, Signal, Slot
from PySide6.QtQml import QmlElement

QML_IMPORT_NAME = "MeleHui"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class SetlistGalleryList(QObject):
    setlistsChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setlists = []
        self._name_filter = ""
        self.refresh()

    def _get_name_filter(self):
        return self._name_filter

    def _set_name_filter(self, name_filter):
        self._name_filter = name_filter
        self.nameFilterChanged.emit()
        self.refresh()

    def _get_setlists(self):
        return list(self._setlists)

    nameFilterChanged = Signal()
    nameFilter = Property(str, _get_name_filter, _set_name_filter, notify=nameFilterChanged)

    setlists = Property(list, _get_setlists, notify=setlistsChanged)

    def get_first_page_or_nil(self, s):
        for ss in s.setlist_songs or []:
            song = getattr(ss, "song", None)
            pages = getattr(song, "pages", None) if song else None
            if pages:
                return QUrl.fromLocalFile(pages[0].file_store.full_path)
        return None

    def refresh(self):
        session = SessionLocal()
        try:
            # rows = session.query(Setlist).all()
            rows = session.query(Setlist).filter(Setlist.name.like("%" + self._name_filter + "%")).all()
            self._setlists = [
                {
                    "id": s.id,
                    "name": s.name,
                    "first_page_img_path": self.get_first_page_or_nil(s),
                }
                for s in rows
            ]
            self.setlistsChanged.emit()
        finally:
            session.close()

    @Slot()
    def reload(self):
        self.refresh()
