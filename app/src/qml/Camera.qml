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
    property int orientation: 0

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

    onPictureAccept: (image, title) => {
        let savedId = CameraBackend.saveCapture(image);
        cameraPage.capturedImage = null;
        pictureSave(savedId, title);
    }

    ColumnLayout {
        anchors.fill: parent

        Controls.Button {
            Layout.alignment: Qt.AlignHCenter
            Layout.fillWidth: true
            text: qsTr("Rotate Camera")
            onClicked: cameraPage.orientation = (cameraPage.orientation + 90) % 360
        }

        VideoOutput {
            id: viewfinder
            orientation: cameraPage.orientation
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
        image: cameraPage.capturedImage
        previewUrl: cameraPage.previewUrl
        orientation: cameraPage.orientation
        onPictureAccept: (image, title) => cameraPage.pictureAccept(CameraBackend.rotateImage(image, cameraPage.orientation), title)
    }
}
