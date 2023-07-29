from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsPolygonItem, QGraphicsRectItem
from PyQt5.QtGui import QPixmap, QPainterPath, QPen
from PyQt5.QtCore import Qt, QRectF, QPointF

class MyGraphicsView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)

    def mousePressEvent(self, event):
        point = event.pos()
        items = self.items(point)
        for item in items:
            if isinstance(item, QGraphicsPolygonItem):
                print("Polygon item clicked!")
            elif isinstance(item, QGraphicsRectItem):
                print("Rect item clicked!")

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.scene = QGraphicsScene()

        # Load your image
        pixmap = QPixmap("images/gimp/PA-Spine.png")
        self.scene.addPixmap(pixmap)

        # Create a red outline pen
        pen = QPen(Qt.red)
        pen.setWidth(2)

        # Define clickable region 1
        rect = QRectF(12, 39, 41, 76)  # Adjust these values as needed y1, y2, x1, x2
        rect_item = self.scene.addRect(rect, pen)

        # Define clickable region 2
        path = QPainterPath()
        path.moveTo(QPointF(40, 250))    # Adjust these values as needed x,y
        path.lineTo(QPointF(120, 350))
        path.lineTo(QPointF(80, 450))
        path.lineTo(QPointF(40, 350))
        path.closeSubpath()
        polygon_item = self.scene.addPath(path, pen)

        self.view = MyGraphicsView(self.scene)
        self.setCentralWidget(self.view)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
