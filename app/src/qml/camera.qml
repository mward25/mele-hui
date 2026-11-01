import QtQuick
import QtQuick.Layouts
import QtQuick.Controls as Controls
import QtMultimedia
import org.kde.kirigami as Kirigami

Kirigami.Page {
    title: qsTr("Capture Picture")

    CaptureSession {
        id: captureSession
        camera: Camera { id: camera; active: true }
        videoOutput: viewfinder
        imageCapture: ImageCapture { id: imageCapture }
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
}
