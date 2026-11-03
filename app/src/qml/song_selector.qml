import QtQuick
import QtQuick.Layouts
import QtQuick.Controls as Controls
import org.kde.kirigami as Kirigami
import MeleHui 1.0

Kirigami.Page {
    id: root
    title: qsTr("Song Selector")

    signal songSelected(int songId)

    SongGalleryList {
        id: songList
    }

    Kirigami.CardsLayout {
        anchors.fill: parent
        Repeater {
            model: songList.songs
            Kirigami.Card {
                actions: [
                    Kirigami.Action {
                        text: qsTr("Select")
                        onTriggered: {
                            root.songSelected(modelData.id);
                            console.log('Trigger action!')
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
