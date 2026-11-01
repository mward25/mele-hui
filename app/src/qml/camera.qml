import QtQuick
import QtQuick.Layouts
import QtQuick.Controls as Controls
import QtMultimedia
import org.kde.kirigami as Kirigami

Kirigami.Page {
    id: cameraPage
    title: qsTr("Capture Picture")

    signal pictureAccept(var image)

    property var capturedImage: null
    property string previewUrl: ""

    CaptureSession {
        id: captureSession
        camera: Camera { id: camera; active: true }
        videoOutput: viewfinder
        imageCapture: ImageCapture {
            id: imageCapture
            onImageCaptured: (requestId, preview) => {
                cameraPage.capturedImage = preview
                cameraPage.previewUrl = CameraBackend.imageToDataUrl(preview)
                saveDialog.open()
            }
        }
    }

    onPictureAccept: (image) => {
        CameraBackend.saveCapture(image)
        cameraPage.capturedImage = null
    }

    ColumnLayout {
        anchors.fill: parent

        VideoOutput {
            id: viewfinder
            Layout.fillWidth: true
            Layout.fillHeight: true
        }

        Controls.Button {
            Layout.alignment: Qt.AlignHCenter
            Layout.fillWidth: true
            text: qsTr("Capture")
            onClicked: imageCapture.capture()
        }
    }

    Kirigami.Dialog {
        id: saveDialog
        title: qsTr("Save Picture")
        modal: true
        anchors.centerIn: parent

        ColumnLayout {
            Image {
                source: cameraPage.previewUrl
                fillMode: Image.PreserveAspectFit
                Layout.preferredWidth: 320
                Layout.preferredHeight: 240
            }
        }
        standardButtons: Kirigami.Dialog.NoButton
        flatFooterButtons: false
        customFooterActions: [
            Kirigami.Action {
                text: qsTr("Yes")
                onTriggered: {
                    cameraPage.pictureAccept(cameraPage.capturedImage)
                    saveDialog.close()
                }
            },
            Kirigami.Action {
                text: qsTr("No, Retake")
                onTriggered: saveDialog.close()
            }
        ]

        onClosed: cameraPage.capturedImage = null
    }
}
