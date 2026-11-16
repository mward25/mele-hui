import QtQuick
import QtQuick.Layouts
import QtQuick.Controls as Controls
import org.kde.kirigami as Kirigami
import MeleHui 1.0

Kirigami.Page {
    id: root
    title: qsTr("New Song")

    signal songCreated(var id)

    SongBackend {
        id: songBackend
    }

    property string songName: ""

    Kirigami.FormLayout {
        anchors.fill: parent

        Kirigami.Separator {
            Kirigami.FormData.label: "Song Info"
            Kirigami.FormData.isSection: true
        }
        Controls.TextField {
            id: songNameField
            text: root.songName
            onTextChanged: root.songName = text
        }
        Kirigami.Separator {
            Kirigami.FormData.label: "Pages"
            Kirigami.FormData.isSection: true
        }
        Controls.Button {
            text: "From Camera"
            icon.name: "camera-symbolic"
            Kirigami.FormData.label: "Add Page:"
            onClicked: {
                const page = pageStack.push(Qt.resolvedUrl("Camera.qml"));
                page.pictureSave.connect((id, title) => {
                    songBackend.addPage(id);
                    if (root.songName == "") {
                        root.songName = title;
                    }
                    pageStack.pop();
                });
            }
        }
        Controls.Button {
            icon.name: "user-images-symbolic"
            text: "From Image"
            onClicked: {
                const page = pageStack.push(Qt.resolvedUrl("ImagePicker.qml"));
                page.pictureSave.connect((id, title) => {
                    songBackend.addPage(id);
                    if (root.songName == "") {
                        root.songName = title;
                    }
                    pageStack.pop();
                });
            }
        }
        Controls.Button {
            icon.name: "emblem-documents-symbolic"
            text: "From PDF"
            onClicked: {
                const page = pageStack.push(Qt.resolvedUrl("PdfPicker.qml"));
                page.pictureSave.connect((id, title) => {
                    songBackend.addPage(id);
                    if (root.songName == "" && title) {
                        root.songName = title;
                    }
                });
            }
        }
        Controls.Label {
            text: "Pages added: " + songBackend.pages.length
        }
        Kirigami.Separator {
            Kirigami.FormData.label: "Finishing Up"
            Kirigami.FormData.isSection: true
        }
        Controls.Button {
            text: "Submit"
            onClicked: {
                const id = songBackend.createSong(root.songName, songBackend.pages);
                if (id > 0) {
                    root.songName = "";
                    songBackend.clear();
                    pageStack.pop();
                }
                root.songCreated(id);
            }
        }
    }
}
