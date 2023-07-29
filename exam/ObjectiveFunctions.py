from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class HealthHistory(QWidget):
    def __init__(self, parent=None):
        super(HealthHistory, self).__init__(parent)
        self.setWindowTitle("Health History Details")
        layout = QVBoxLayout()
        label = QLabel("Here you can display the health history details.")
        layout.addWidget(label)
        self.setLayout(layout)
