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
            id: songList
            Layout.fillWidth: true
            Layout.fillHeight: true
            model: setlistView
            moveDisplaced: Transition {
                YAnimator {
                    duration: Kirigami.Units.longDuration
                    easing.type: Easing.InOutQuad
                }
            }
            delegate: Item {
                id: listItemRoot

                required property int index
                required property string name

                width: songList.width - songList.leftMargin - songList.rightMargin
                height: item.implicitHeight

                Controls.ItemDelegate {
                    id: item
                    width: listItemRoot.width
                    contentItem: RowLayout {
                        Kirigami.ListItemDragHandle {
                            listItem: item
                            listView: songList
                            onMoveRequested: (oldIndex, newIndex) => {
                                setlistView.moveSong(oldIndex, newIndex);
                            }
                        }
                        Controls.Label {
                            Layout.fillWidth: true
                            text: listItemRoot.name
                        }
                    }
                }
            }
        }
    }
}
