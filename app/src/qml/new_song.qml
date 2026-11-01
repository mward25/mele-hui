import QtQuick
import QtQuick.Layouts
import QtQuick.Controls as Controls
import org.kde.kirigami as Kirigami
import MeleHui 1.0

Kirigami.Page {
    id: root
    title: qsTr("New Song")

    SongBackend { id: songBackend }

    property string songName: ""

    Kirigami.FormLayout {
        anchors.fill: parent

        Kirigami.Separator { Kirigami.FormData.label: "Song Info"; Kirigami.FormData.isSection: true }
        Controls.TextField {
            Kirigami.FormData.label: "Song Name:"
            text: root.songName
            onTextChanged: root.songName = text
        }
        Kirigami.Separator { Kirigami.FormData.label: "Pages"; Kirigami.FormData.isSection: true }
        Controls.Button {
            text: "Add page"
            Kirigami.FormData.label: "Add Page:"
            onClicked: {
                const page = pageStack.push(Qt.resolvedUrl("camera.qml"))
                page.pictureSave.connect((id) => {
                    songBackend.addPage(id)
                    pageStack.pop()
                })
            }
        }
        Controls.Label {
            text: "Pages added: " + songBackend.pages.length
        }
        Kirigami.Separator { Kirigami.FormData.label: "Finishing Up"; Kirigami.FormData.isSection: true }
        Controls.Button {
            text: "Submit"
            onClicked: {
                const id = songBackend.createSong(root.songName, songBackend.pages)
                if (id > 0) {
                    root.songName = ""
                    songBackend.clear()
                    pageStack.pop()
                }
            }
        }
    }
}
