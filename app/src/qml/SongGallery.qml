import QtQuick
import QtQuick.Layouts
import QtQuick.Controls as Controls
import org.kde.kirigami as Kirigami
import MeleHui 1.0

Kirigami.Page {
    id: root
    title: qsTr("Song Gallery")

    SongGalleryList {
        id: songList
        nameFilter: filterField.text
    }

    ColumnLayout {
        anchors.fill: parent
        Controls.TextField {
            id: filterField
            Layout.fillWidth: true
            placeholderText: "Filter Songs"
        }
        Flickable {
            Layout.fillWidth: true
            Layout.fillHeight: true
            contentWidth: width
            contentHeight: cards.implicitHeight
            Kirigami.CardsLayout {
                id: cards
                width: parent.width
                Repeater {
                    model: songList.songs
                    Kirigami.Card {
                        actions: [
                            Kirigami.Action {
                                text: qsTr("Open")
                                onTriggered: {
                                    pageStack.layers.push(Qt.resolvedUrl("SongViewer.qml"), {
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
    }
}
