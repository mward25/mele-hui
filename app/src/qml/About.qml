import QtQuick
import QtQuick.Layouts
import QtQuick.Controls as Controls
import org.kde.kirigami as Kirigami

Kirigami.ScrollablePage {
    id: root
    title: qsTr("About Mele Hui")

    property string licenseText: "Mele Hui, A sheet music reading & organization program.\nCopyright (C) 2026  Miles Ward\n\nThis program is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version."

    ColumnLayout {
        width: root.width
        spacing: Kirigami.Units.smallSpacing

        Kirigami.Card {
            banner {
                title: qsTr("Mele Hui")
            }
            width: parent.width

            contentItem: ColumnLayout {
                spacing: Kirigami.Units.smallSpacing
                Controls.Label {
                    text: qsTr("A simple sheet music reading program.")
                    wrapMode: Text.WordWrap
                    Layout.fillWidth: true
                }
                Controls.Label {
                    text: qsTr("Author: Miles Ward")
                    Layout.fillWidth: true
                }
                Controls.Label {
                    text: qsTr("Homepage: https://github.com/mward25/mele-hui")
                    Layout.fillWidth: true
                }
                Controls.Label {
                    text: qsTr("License: GNU General Public License v3 or later (GPLv3+)")
                    Layout.fillWidth: true
                }
            }
            actions: [
                Kirigami.Action {
                    text: "Open License"
                    onTriggered: {
                        /// Open https://github.com/mward25/mele-hui/blob/main/LICENSE
                        Qt.openUrlExternally("https://github.com/mward25/mele-hui/blob/main/LICENSE");
                    }
                },
                Kirigami.Action {
                    text: "Open Repo/Homepage"
                    onTriggered: {
                        /// Open https://github.com/mward25/mele-hui
                        Qt.openUrlExternally("https://github.com/mward25/mele-hui");
                    }
                }
            ]
        }

        Kirigami.Card {
            banner {
                title: qsTr("License")
            }
            width: parent.width

            contentItem: Controls.Label {
                text: root.licenseText
                wrapMode: Text.WrapAnywhere
                Layout.fillWidth: true
                font.family: "monospace"
                font.pointSize: 8
            }
        }
    }
}
