import QtQuick
import QtQuick.Layouts
import QtQuick.Controls as Controls
import org.kde.kirigami as Kirigami
import MeleHui 1.0

Kirigami.Page {
    id: root
    title: qsTr("New Song")

    SetlistBackend {
        id: setlistBackend
    }

    property string setlistName: ""

    Kirigami.FormLayout {
        anchors.fill: parent

        Controls.TextField {
            id: setlistNameField
            Kirigami.FormData.label: "Setlist Name"
            text: root.setlistName
            onTextChanged: root.setlistName = text
        }

        Controls.Button {
            text: "Submit"
            onClicked: {
                const id = setlistBackend.createSetlist(root.setlistName);
                if (id > 0) {
                    root.setlistName = "";
                    setlistBackend.clear();
                    pageStack.pop();
                }
            }
        }
    }
}
