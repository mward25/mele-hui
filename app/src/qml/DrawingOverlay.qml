import QtQuick
import QtQuick.Controls as Controls
import org.kde.kirigami as Kirigami
import MeleHui 1.0

Item {
    id: root
    property int pageId: 0
    property var backend: null
    property string tool: "none"  // "none" | "pen" | "eraser"
    property bool drawingActive: false
    property real penWidth: 3
    property string penColor: "#111111"

    property var strokes: []
    property string currentStroke: ""

    signal svgChanged(string svg)


    function loadSvg(svg) {
        if (backend !== null) strokes = backend.svgToStrokes(svg || "");
        else strokes = [];
        canvas.requestPaint();
    }

    function save() {
        let svg = (backend !== null) ? backend.strokesToSvg(width, height, strokes) : "";
        svgChanged(svg);
        if (backend !== null && pageId > 0) backend.saveDrawing(pageId, svg);
    }

    function clear() { strokes = []; canvas.requestPaint(); }

    onBackendChanged: if (backend !== null && pageId > 0) loadSvg(backend.drawingForPage(pageId));
    onPageIdChanged: if (backend !== null && pageId > 0) loadSvg(backend.drawingForPage(pageId));

    Canvas {
        id: canvas
        anchors.fill: parent
        onPaint: {
            let ctx = getContext("2d");
            ctx.clearRect(0, 0, width, height);
            for (let i = 0; i < root.strokes.length; i++) {
                let s = root.strokes[i];
                if (!s.points || s.points.length < 2) continue;
                ctx.beginPath();
                ctx.moveTo(s.points[0].x, s.points[0].y);
                for (let j = 1; j < s.points.length; j++) ctx.lineTo(s.points[j].x, s.points[j].y);
                if (s.mode === "eraser") {
                    ctx.globalCompositeOperation = "destination-out";
                    ctx.lineWidth = root.penWidth * 2;
                } else {
                    ctx.globalCompositeOperation = "source-over";
                    ctx.strokeStyle = root.penColor;
                    ctx.lineWidth = root.penWidth;
                }
                ctx.lineCap = "round";
                ctx.lineJoin = "round";
                ctx.stroke();
            }
            ctx.globalCompositeOperation = "source-over";
        }
    }

    MouseArea {
        anchors.fill: parent
        onPressed: (mouse) => {
            if (root.tool === "none") return;
            root.drawingActive = true;
            root.currentStroke = root.tool;
            let pts = [{ x: mouse.x, y: mouse.y }];
            root.strokes.push({ mode: root.currentStroke, points: pts });
        }
        onPositionChanged: (mouse) => {
            if (!pressed || root.tool === "none") return;
            let last = root.strokes[root.strokes.length - 1];
            last.points.push({ x: mouse.x, y: mouse.y });
            canvas.requestPaint();
        }
        onReleased: (mouse) => {
            if (!root.drawingActive) return;
            root.drawingActive = false;
            root.save();
        }
    }

    Row {
        spacing: 8
        Controls.Button { text: root.tool === "pen" ? "Pen ✓" : "Pen"; onClicked: root.tool = (root.tool === "pen" ? "none" : "pen") }
        Controls.Button { text: root.tool === "eraser" ? "Erase ✓" : "Erase"; onClicked: root.tool = (root.tool === "eraser" ? "none" : "eraser") }
        Controls.Button { text: "Clear"; onClicked: root.clear() }
    }
}
