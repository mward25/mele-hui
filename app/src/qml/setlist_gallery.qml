import QtQuick
import QtQuick.Layouts
import QtQuick.Controls as Controls
import org.kde.kirigami as Kirigami
import MeleHui 1.0

Kirigami.Page {
    id: root
    title: qsTr("Setlist Gallery")

    SetlistGalleryList {
        id: setlistList
    }

    Kirigami.CardsLayout {
        anchors.fill: parent
        Repeater {
            model: setlistList.setlists
            Kirigami.Card {
                actions: [
                    Kirigami.Action {
                        text: qsTr("Open")
                        onTriggered: {
                            pageStack.push(Qt.resolvedUrl("setlist_viewer.qml"), {
                                "setlistId": modelData.id
                            });
                        }
                    }
                ]
                banner {
                    title: modelData.name
                }
            }
        }
    }
}
