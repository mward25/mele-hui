import org.kde.kirigami as Kirigami
import QtCore
import QtQuick
import QtQuick.Layouts
import QtQuick.Dialogs as QQC2Dialogs
import MeleHui 1.0

Kirigami.Page {
    id: root
    title: qsTr("Pick A Picture")

    signal pictureSave(var id, var title)
    signal pictureAccept(var image, var title)

    onPictureAccept: (image, title) => {
        let savedId = CameraBackend.saveCapture(image);
        root.pictureSave(savedId, title);
    }

    ColumnLayout {
        Image {
            id: image
            fillMode: Image.PreserveAspectFit
        }

        QQC2Dialogs.FileDialog {
            id: fileDialog
            currentFolder: StandardPaths.standardLocations(StandardPaths.PicturesLocation)[0]
            nameFilters: ["Image files (*.png *.jpg *.jpeg *.bmp *.gif *.svg)"]
            onAccepted: {
                image.source = selectedFile;
                saveDialog.previewUrl = selectedFile;
                saveDialog.open();
            }
            onRejected: {
                /// On reject, just exit this page (assume it was user mistake)
                pageStack.pop();
            }
            Component.onCompleted: {
                Qt.callLater(fileDialog.open);
            }
        }
    }

    PageConfirmDialog {
        id: saveDialog
        image: CameraBackend.rotateImage(CameraBackend.loadImage(image.source), 0)
        previewUrl: image.source
        onPictureAccept: (image, title) => root.pictureAccept(image, title)
    }
}
