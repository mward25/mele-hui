import QtQuick
import QtQuick.Controls as Controls
import org.kde.kirigami as Kirigami

Row {
    id: root
    property var target: null
    spacing: 8
    padding: 8

    Controls.Button {
        text: (root.target && root.target.drawingTool === "pen") ? "Pen ✓" : "Pen"
        onClicked: if (root.target)
            root.target.drawingTool = (root.target.drawingTool === "pen" ? "none" : "pen")
    }
    Controls.Button {
        text: (root.target && root.target.drawingTool === "eraser") ? "Erase ✓" : "Erase"
        onClicked: if (root.target)
            root.target.drawingTool = (root.target.drawingTool === "eraser" ? "none" : "eraser")
    }
    Controls.Button {
        text: "Clear"
        onClicked: if (root.target && root.target.drawingOverlay)
            root.target.drawingOverlay.clear()
    }
}
