import QtQuick
import QtQuick.Layouts
import QtQuick.Controls as Controls
import org.kde.kirigami as Kirigami

Kirigami.ApplicationWindow {
    id: root

    title: qsTr("Simple Markdown viewer")

    minimumWidth: Kirigami.Units.gridUnit * 20
    minimumHeight: Kirigami.Units.gridUnit * 20
    width: minimumWidth
    height: minimumHeight

    pageStack.initialPage: initPage
    // globalDrawer: Kirigami.GlobalDrawer {
    //     title: "Global Drawer"
    //     titleIcon: "applications-graphics"
    //     actions: [
    //         Kirigami.Action {
    //             text: "Home"
    //             icon.name: "user-home-symbolic"
    //             // onTriggered: showPassiveNotification("Action 1 clicked")
    //         },
    //         // Kirigami.Action {
    //         //     text: "Kirigami Action 2"
    //         //     icon.name: "settings-configure-symbolic"
    //         //     onTriggered: showPassiveNotification("Action 2 clicked")
    //         // },
    //         Kirigami.Action {
    //             text: i18n("Quit")
    //             icon.name: "application-exit-symbolic"
    //             shortcut: StandardKey.Quit
    //             onTriggered: Qt.quit()
    //         }
    //     ]
    // }
    Component {
        id: initPage

        Kirigami.Page {
            title: qsTr("Mele Hui Home")

            ColumnLayout {
                anchors {
                    top: parent.top
                    left: parent.left
                    right: parent.right
                }
                Kirigami.Heading {
                    text: "Quick Actions"
                    Layout.alignment: Qt.AlignHCenter
                }
                Controls.Button {
                    Layout.alignment: Qt.AlignHCenter
                    Layout.fillWidth: true
                    text: qsTr("Take Picture")
                    onClicked: pageStack.push(Qt.resolvedUrl("camera.qml"))
                }
                Controls.Button {
                    Layout.alignment: Qt.AlignHCenter
                    Layout.fillWidth: true
                    text: qsTr("Create Song")
                    onClicked: pageStack.push(Qt.resolvedUrl("new_song.qml"))
                }
            }
        }
    }
    footer: Kirigami.NavigationTabBar {
    }
}
