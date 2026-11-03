import QtQuick
import QtQuick.Layouts
import QtQuick.Controls as Controls
import org.kde.kirigami as Kirigami
import MeleHui 1.0

Kirigami.Page {
    id: root
    title: qsTr("Song Gallery")

    SongGaleryList {
        id: songList
    }

    Kirigami.CardsLayout {
        anchors.fill: parent
        Repeater {
            model: songList.songs
            Kirigami.Card {
                actions: [
                    Kirigami.Action {
                        text: qsTr("Open")
                        onTriggered: {
                            pageStack.push(Qt.resolvedUrl("song_viewer.qml"), {
                                "songId": modelData.id
                            });
                        }
                    }
                ]
                banner {
                    source: modelData.first_page_img_path != null ? modelData.first_page_img_path : ""
                    title: modelData.name
                }
            }
        }
    }
}
