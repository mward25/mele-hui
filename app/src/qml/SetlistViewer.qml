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
    actions: [
        Kirigami.Action {
            text: "Create New Song"
            icon.name: "document-new"
            onTriggered: {
                var page = pageStack.push(Qt.resolvedUrl("NewSong.qml"));
                page.songCreated.connect(function (songId) {
                    setlistView.addSong(songId);
                    pageStack.pop();
                });
            }
        },
        Kirigami.Action {
            text: "Add Existing Song"
            icon.name: "document-import-symbolic"
            onTriggered: {
                var page = pageStack.push(Qt.resolvedUrl("SongSelector.qml"));
                page.songSelected.connect(function (songId) {
                    setlistView.addSong(songId);
                    pageStack.pop();
                });
            }
        }
    ]

    ColumnLayout {
        anchors.fill: parent
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
                required property int id
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

                        Controls.Button {
                            text: qsTr("Open")
                            onClicked: pageStack.layers.push(Qt.resolvedUrl("SongViewer.qml"), {
                                songId: listItemRoot.id
                            })
                        }
                    }
                }
            }
        }
    }
}
