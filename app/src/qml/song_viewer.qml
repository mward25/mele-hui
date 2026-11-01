import QtQuick
import QtQuick.Layouts
import QtQuick.Controls as Controls
import org.kde.kirigami as Kirigami
import MeleHui 1.0

Kirigami.Page {
    id: root
    title: qsTr("Song Viewer (" + songView.song.name + ")")
    required property var songId
    SongView {
        id: songView
        songId: root.songId
    }
    
    ListView {
        id: pageList
        anchors.fill: parent
        visible: songView.pages.length > 0
        orientation: ListView.Horizontal
        snapMode: ListView.SnapOneItem
        highlightRangeMode: ListView.StrictlyEnforceRange
        clip: true
        model: songView.pages
        delegate: Item {
            width: pageList.width
            height: pageList.height
            Image {
                anchors.fill: parent
                fillMode: Image.PreserveAspectFit
                source: modelData.file_path
            }
        }
    }
}
