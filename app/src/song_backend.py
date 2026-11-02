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

    @Slot(int, str)
    def saveDrawing(self, page_id: int, svg: str) -> None:
        session = SessionLocal()
        try:
            page = session.get(Page, page_id)
            if page is not None:
                page.drawing_svg = (svg or "").strip() or None
                session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @Slot(int, result=str)
    def drawingForPage(self, page_id: int) -> str:
        session = SessionLocal()
        try:
            page = session.get(Page, page_id)
            return (page.drawing_svg if page is not None and page.drawing_svg else "")
        finally:
            session.close()

    @Slot(int, int, "QVariantList", result=str)
    def strokesToSvg(self, width: int, height: int, strokes) -> str:
        width = width or 1
        height = height or 1
        out = ["<svg xmlns='http://www.w3.org/2000/svg' width='%d' height='%d'>" % (width, height)]
        for stroke in (strokes or []):
            pts = stroke.get("points") if isinstance(stroke, dict) else None
            if not pts or len(pts) < 2:
                continue
            mode = stroke.get("mode", "pen") if isinstance(stroke, dict) else "pen"
            d = "M %s %s" % (pts[0]["x"], pts[0]["y"])
            for pt in pts[1:]:
                d += " L %s %s" % (pt["x"], pt["y"])
            if mode == "erase":
                out.append("<path d='%s' fill='none' stroke='none' stroke-width='0' data-mode='erase'/>" % d)
            else:
                out.append("<path d='%s' fill='none' stroke='#e01b24' stroke-width='3' stroke-linecap='round' stroke-linejoin='round' data-mode='pen'/>" % d)
        out.append("</svg>")
        return "".join(out)

    @Slot(str, result="QVariantList")
    def svgToStrokes(self, svg: str):
        import re
        strokes = []
        for m in re.finditer(r"<path[^>]*d='([^']*)'[^>]*data-mode='([^']*)'", svg or ""):
            d = m.group(1)
            mode = m.group(2)
            pts = []
            toks = d.split()
            i = 0
            while i < len(toks):
                if toks[i] in ("M", "L") and i + 2 < len(toks):
                    try:
                        x = float(toks[i+1]); y = float(toks[i+2])
                        pts.append({"x": x, "y": y})
                    except ValueError:
                        pass
                    i += 3
                else:
                    i += 1
            if len(pts) >= 2:
                strokes.append({"mode": mode, "points": pts})
        return strokes

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
