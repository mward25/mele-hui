import QtQuick
import QtQuick.Layouts
import QtQuick.Controls as Controls
import QtMultimedia
import org.kde.kirigami as Kirigami
import MeleHui 1.0

Kirigami.Dialog {
    id: root

    signal pictureAccept(var image, var title)

    property var image: null
    property string previewUrl: ""

    AutoCropper {
        id: defaultCropper
        image: root.image
    }
    AutoNamer {
        id: defaultAutoNamer
        image: defaultCropper.croppedImage
    }

    property var autoNamer: defaultAutoNamer
    property var autoCropper: defaultCropper

    title: qsTr("Save Picture")
    modal: true
    anchors.centerIn: parent

    ColumnLayout {
        Kirigami.Heading {
            text: root.autoNamer.title ? root.autoNamer.title : "No title detected"
        }
        Image {
            source: root.previewUrl
            fillMode: Image.PreserveAspectFit
            Layout.preferredWidth: 320
            Layout.preferredHeight: 240
        }
        Image {
            source: (root.autoCropper.croppedImage == null) ? "" : CameraBackend.imageToDataUrl(root.autoCropper.croppedImage)
            fillMode: Image.PreserveAspectFit
            Layout.preferredWidth: 320
            Layout.preferredHeight: 240
        }
    }
    standardButtons: Kirigami.Dialog.NoButton
    flatFooterButtons: false
    customFooterActions: [
        Kirigami.Action {
            text: qsTr("Yes, cropped")
            onTriggered: {
                root.pictureAccept(root.autoCropper.croppedImage, root.autoNamer.title);
                root.close();
            }
        },
        Kirigami.Action {
            text: qsTr("Yes, uncropped")
            onTriggered: {
                root.pictureAccept(root.image, root.autoNamer.title);
                root.close();
            }
        },
        Kirigami.Action {
            text: qsTr("No, Retake")
            onTriggered: root.close()
        }
    ]
}
