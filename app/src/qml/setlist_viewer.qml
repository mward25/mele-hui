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

    ListView {
        anchors.fill: parent
        model: setlistView
        delegate: Controls.Label {
            text: model.name
        }
    }
}
