from db import Song
from db.session import SessionLocal
from PySide6.QtCore import Property, QObject, QUrl, Signal, Slot
from PySide6.QtQml import QmlElement

QML_IMPORT_NAME = "MeleHui"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class SongGalleryList(QObject):
    songsChanged = Signal()

    def _get_name_filter(self):
        return self._name_filter

    def _set_name_filter(self, name_filter):
        self._name_filter = name_filter
        self.nameFilterChanged.emit()
        self.refresh()

    nameFilterChanged = Signal()
    nameFilter = Property(str, _get_name_filter, _set_name_filter, notify=nameFilterChanged)

    def _get_filter_by_needs_practice(self):
        return self._filter_by_needs_practice

    def _set_filter_by_needs_practice(self, filter_by_needs_practice):
        self._filter_by_needs_practice = filter_by_needs_practice
        self.filterByNeedsPracticeChanged.emit()
        self.refresh()

    filterByNeedsPracticeChanged = Signal()
    filterByNeedsPractice = Property(bool, _get_filter_by_needs_practice, _set_filter_by_needs_practice, notify=filterByNeedsPracticeChanged)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._songs = []
        self._name_filter = ""
        self._filter_by_needs_practice = False
        self.refresh()

    def _get_songs(self):
        return list(self._songs)

    songs = Property(list, _get_songs, notify=songsChanged)

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
            rows = session.query(Song)
            if self._name_filter != "":
                rows = rows.filter(Song.name.like("%" + self._name_filter + "%"))
            if self._filter_by_needs_practice:
                rows = rows.filter(Song.needs_practice)
            rows = rows.all()
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
