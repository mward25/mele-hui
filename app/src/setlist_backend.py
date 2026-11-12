from db import Setlist
from db.session import SessionLocal
from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtQml import QmlElement

QML_IMPORT_NAME = "MeleHui"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class SetlistBackend(QObject):
    songsChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot()
    def clear(self) -> None:
        pass

    @Slot(str, result=int)
    def createSetlist(self, name: str) -> int:
        name = (name or "").strip()
        if not name:
            return -1
        session = SessionLocal()
        try:
            setlist = Setlist(name=name)
            session.add(setlist)
            session.flush()
            session.commit()
            return setlist.id
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
