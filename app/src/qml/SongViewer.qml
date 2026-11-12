import QtQuick
import QtQuick.Layouts
import QtQuick.Controls as Controls
import org.kde.kirigami as Kirigami
import MeleHui 1.0

Kirigami.ScrollablePage {
    id: root
    required property var songId
    title: qsTr("Song Viewer (" + (songView.song ? songView.song.name : "") + ")")

    SongBackend {
        id: songBackend
    }
    SongView {
        id: songView
        songId: root.songId
    }

    ListView {
        id: pageList
        focus: true
        anchors.fill: parent
        visible: songView.pages && songView.pages.length > 0
        orientation: ListView.Vertical
        snapMode: ListView.NoSnap
        interactive: !(pageList.currentItem && pageList.currentItem.drawingTool !== "none")
        Keys.onPressed: event => {
            if (event.key === Qt.Key_PageUp)
                contentY = Math.max(0, contentY - height / 2);
            else if (event.key === Qt.Key_PageDown)
                contentY = Math.min(contentHeight - height, contentY + height / 2);
        }
        clip: true
        model: songView.pages
        delegate: Item {
            width: pageList.width
            height: (pageImage.sourceSize.width > 0) ? Math.round(pageList.width * pageImage.sourceSize.height / pageImage.sourceSize.width) : pageList.height
            property alias drawingActive: drawingOverlay.drawingActive
            property alias drawingTool: drawingOverlay.tool
            Image {
                id: pageImage
                anchors.fill: parent
                fillMode: Image.Stretch
                source: modelData.file_path
            }
            DrawingOverlay {
                id: drawingOverlay
                anchors.fill: pageImage
                onActivated: pageList.currentIndex = index
                pageId: modelData.id
                pageIndex: index
                backend: songBackend
            }
        }
    }
}
