#!/usr/bin/env python3

import os
import sys
import signal

from PySide6.QtGui import QGuiApplication

from PySide6.QtCore import QUrl

from PySide6.QtQml import QQmlApplicationEngine

from camera_backend import CameraBackend
from song_backend import SongBackend
from song_gallery_list import SongGalleryList
from song_view import SongView
from auto_cropper import AutoCropper
from auto_namer import AutoNamer
from setlist_gallery_list import SetlistGalleryList
from setlist_backend import SetlistBackend
from PySide6.QtQml import qmlRegisterType
from db.session import init_db


def main():
    """Initializes and manages the application execution"""
    app = QGuiApplication(sys.argv)
    init_db()
    engine = QQmlApplicationEngine()
    qmlRegisterType(SongBackend, "MeleHui", 1, 0, "SongBackend")
    qmlRegisterType(SongGalleryList, "MeleHui", 1, 0, "SongGalleryList")
    qmlRegisterType(SongView, "MeleHui", 1, 0, "SongView")
    qmlRegisterType(AutoCropper, "MeleHui", 1, 0, "AutoCropper")
    qmlRegisterType(AutoNamer, "MeleHui", 1, 0, "AutoNamer")
    qmlRegisterType(SetlistBackend, "MeleHui", 1, 0, "SetlistBackend")
    qmlRegisterType(SetlistGalleryList, "MeleHui", 1, 0, "SetlistGalleryList")
    camera_backend = CameraBackend()
    song_backend = SongBackend()
    engine.rootContext().setContextProperty("CameraBackend", camera_backend)
    engine.rootContext().setContextProperty("SongBackend", song_backend)
    # keep reference alive
    engine._camera_backend = camera_backend
    engine._song_backend = song_backend

    """Needed to close the app with Ctrl+C"""
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    """Needed to get proper KDE style outside of Plasma"""
    if not os.environ.get("QT_QUICK_CONTROLS_STYLE"):
        os.environ["QT_QUICK_CONTROLS_STYLE"] = "org.kde.desktop"

    base_path = os.path.abspath(os.path.dirname(__file__))
    url = QUrl(f"file://{base_path}/qml/main.qml")
    engine.load(url)

    if len(engine.rootObjects()) == 0:
        quit()

    app.exec()


if __name__ == "__main__":
    main()
