import QtQuick
import QtQuick.Controls as Controls
import QtQuick.Layouts
import org.kde.kirigami as Kirigami
import MeleHui 1.0

Kirigami.Page {
    id: root

    property int setlistId: 0

    SetlistView {
        id: setlistView
        setlistId: root.setlistId
    }

    ColumnLayout {
        anchors.fill: parent
        Controls.Button {
            text: qsTr("Add Song")
            onClicked: {
                var page = pageStack.push(Qt.resolvedUrl("song_selector.qml"));
                page.songSelected.connect(function(songId) {
                    setlistView.addSong(songId);
                    pageStack.pop();
                });
            }
        }
        ListView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            model: setlistView
            delegate: Controls.Label {
                text: model.name
            }
        }
    }
}
