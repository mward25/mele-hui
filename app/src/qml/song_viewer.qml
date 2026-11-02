import QtQuick
import QtQuick.Layouts
import QtQuick.Controls as Controls
import org.kde.kirigami as Kirigami
import MeleHui 1.0

Kirigami.Page {
    id: root
    required property var songId
    title: qsTr("Song Viewer (" + (songView.song ? songView.song.name : "") + ")")

    SongBackend { id: songBackend }
    SongView {
        id: songView
        songId: root.songId
    }

    ListView {
        id: pageList
        anchors.fill: parent
        visible: songView.pages && songView.pages.length > 0
        orientation: ListView.Horizontal
        snapMode: ListView.SnapOneItem
        interactive: !(currentItem && currentItem.drawingActive)
        highlightRangeMode: ListView.StrictlyEnforceRange
        clip: true
        model: songView.pages
        delegate: Item {
            width: pageList.width
            height: pageList.height
            property alias drawingActive: drawingOverlay.drawingActive
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
