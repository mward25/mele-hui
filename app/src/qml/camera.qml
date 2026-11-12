import QtQuick
import QtQuick.Layouts
import QtQuick.Controls as Controls
import QtMultimedia
import org.kde.kirigami as Kirigami
import MeleHui 1.0

Kirigami.Page {
    id: cameraPage
    title: qsTr("Capture Picture")

    signal pictureAccept(var image)
    signal pictureSave(var id, var title)

    property var capturedImage: null
    property string previewUrl: ""

    CaptureSession {
        id: captureSession
        camera: Camera {
            id: camera
            active: true
        }
        videoOutput: viewfinder
        imageCapture: ImageCapture {
            id: imageCapture
            onImageCaptured: (requestId, preview) => {
                cameraPage.capturedImage = preview;
                cameraPage.previewUrl = CameraBackend.imageToDataUrl(preview);
                saveDialog.open();
            }
        }
    }

    onPictureAccept: image => {
        let savedId = CameraBackend.saveCapture(image);
        cameraPage.capturedImage = null;
        pictureSave(savedId, autoNamer.title);
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

    PageConfirmDialog {
        id: saveDialog
        cameraPage: cameraPage
        image: cameraPage.capturedImage
        previewUrl: cameraPage.previewUrl
    }
}
