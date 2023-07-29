from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Assessment(QWidget):
    def __init__(self, parent=None):
        super(Assessment, self).__init__(parent)
        layout = QVBoxLayout(self)

        # Add your widgets to the layout
        self.widget1 = QLabel("Hello Assessment", self)
        self.widget2 = QCheckBox("Check Me", self)

        layout.addWidget(self.widget1)
        layout.addWidget(self.widget2)
        self.setLayout(layout)
