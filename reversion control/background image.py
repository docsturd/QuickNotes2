import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap

class ImageBackgroundApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Background App")
        self.setGeometry(100, 100, 800, 600)  # Set the initial window size

        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, self.width(), self.height())

        self.button = QPushButton("Select Image", self)
        self.button.setGeometry(10, 10, 150, 30)
        self.button.clicked.connect(self.set_background)

    def set_background(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Image files (*.png *.jpg *.jpeg *.gif)")
        file_dialog.setWindowTitle("Select Image File")
        if file_dialog.exec_():
            filenames = file_dialog.selectedFiles()
            if filenames:
                image_file = filenames[0]
                self.background_label.clear()
                pixmap = QPixmap(image_file)
                self.background_label.setPixmap(pixmap.scaled(self.width(), self.height()))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageBackgroundApp()
    window.show()
    sys.exit(app.exec_())
