import QtQuick
import QtQuick.Controls as Controls
import org.kde.kirigami as Kirigami
import MeleHui 1.0

Item {
    id: root
    property int pageId: 0
    property int pageIndex: 0
    property var backend: null
    property string tool: "none"
    property bool drawingActive: false
    property real penWidth: 3
    property string penColor: "#111111"

    property var strokes: []
    property string currentStroke: ""

    signal svgChanged(string svg)
    signal activated

    function loadSvg(svg) {
        if (backend !== null)
            strokes = backend.svgToStrokes(svg || "");
        else
            strokes = [];
        canvas.requestPaint();
    }

    function save() {
        let svg = (backend !== null) ? backend.strokesToSvg(width, height, strokes) : "";
        svgChanged(svg);
        if (backend !== null && pageId > 0)
            backend.saveDrawing(pageId, svg);
    }

    function clear() {
        strokes = [];
        canvas.requestPaint();
    }

    onBackendChanged: if (backend !== null && pageId > 0)
        loadSvg(backend.drawingForPage(pageId))
    onPageIdChanged: if (backend !== null && pageId > 0)
        loadSvg(backend.drawingForPage(pageId))

    Canvas {
        id: canvas
        anchors.fill: parent
        onPaint: {
            let ctx = getContext("2d");
            ctx.clearRect(0, 0, width, height);
            for (let i = 0; i < root.strokes.length; i++) {
                let s = root.strokes[i];
                if (!s.points || s.points.length < 2)
                    continue;
                ctx.beginPath();
                ctx.moveTo(s.points[0].x * canvas.width, s.points[0].y * canvas.height);
                for (let j = 1; j < s.points.length; j++)
                    ctx.lineTo(s.points[j].x * canvas.width, s.points[j].y * canvas.height);
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
        preventStealing: true
        onPressed: mouse => {
            root.activated();
            if (root.tool === "none")
                return;
            root.drawingActive = true;
            root.currentStroke = root.tool;
            let w = Math.max(1, canvas.width);
            let h = Math.max(1, canvas.height);
            let pts = [
                {
                    x: mouse.x / w,
                    y: mouse.y / h
                }
            ];
            root.strokes.push({
                mode: root.currentStroke,
                points: pts
            });
        }
        onPositionChanged: mouse => {
            if (!pressed || root.tool === "none")
                return;
            let last = root.strokes[root.strokes.length - 1];
            let w2 = Math.max(1, canvas.width);
            let h2 = Math.max(1, canvas.height);
            last.points.push({
                x: mouse.x / w2,
                y: mouse.y / h2
            });
            canvas.requestPaint();
        }
        onReleased: mouse => {
            if (!root.drawingActive)
                return;
            root.drawingActive = false;
            canvas.requestPaint();
            root.save();
        }
    }
    Row {
        visible: parent.parent.ListView.view.currentIndex === root.pageIndex
        spacing: 8
        Controls.Button {
            text: root.tool === "pen" ? "Pen ✓" : "Pen"
            onClicked: root.tool = (root.tool === "pen" ? "none" : "pen")
        }
        Controls.Button {
            text: root.tool === "eraser" ? "Erase ✓" : "Erase"
            onClicked: root.tool = (root.tool === "eraser" ? "none" : "eraser")
        }
        Controls.Button {
            text: "Clear"
            onClicked: root.clear()
        }
    }
}
