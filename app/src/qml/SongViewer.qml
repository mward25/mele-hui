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

    header: DrawingToolbar {
        target: pageList.currentItem
    }
    ListView {
        id: pageList
        anchors.fill: parent
        visible: songView.pages && songView.pages.length > 0
        orientation: ListView.Vertical
        snapMode: ListView.NoSnap
        interactive: true
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
                fillMode: Image.PreserveAspectFit
                source: modelData.file_path
            }
            DrawingOverlay {
                id: drawingOverlay
                anchors.fill: pageImage
                pageId: modelData.id
                backend: songBackend
            }
        }
    }
}
