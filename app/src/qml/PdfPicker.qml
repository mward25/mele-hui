import org.kde.kirigami as Kirigami
import QtCore
import QtQuick
import QtQuick.Layouts
import QtQuick.Dialogs as QQC2Dialogs
import MeleHui 1.0

Kirigami.Page {
    id: root
    title: qsTr("Pick A PDF")

    signal pictureSave(var id, var title)
    signal pictureAccept(var image, var title)

    onPictureAccept: (image, title) => {
        let savedId = CameraBackend.saveCapture(image);
        root.pictureSave(savedId, title);
    }

    ColumnLayout {
        QQC2Dialogs.FileDialog {
            id: fileDialog
            currentFolder: StandardPaths.standardLocations(StandardPaths.PicturesLocation)[0]
            nameFilters: ["PDF files (*.pdf)"]
            onAccepted: {
                var images = CameraBackend.pdfToImages(selectedFile);
                var base = selectedFile.toString().split('/').pop().replace(/\.[^.]*$/, "");
                for (var i = 0; i < images.length; i++) {
                    root.pictureAccept(images[i], i === 0 ? base : "");
                }
                pageStack.pop();
            }
            onRejected: {
                pageStack.pop();
            }
            Component.onCompleted: {
                Qt.callLater(fileDialog.open);
            }
        }
    }
}
