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

class BioMetrics(QWidget):
    biometrics = ["Pulse", "Height", "Weight", "POX"]
    def __init__(self, items, items_per_row=1):
        super().__init__()
        self.setWindowTitle('Biometric Window')
        self.main_layout = QVBoxLayout()
        
        # Use the provided function to create the group box
        groupbox = self.create_groupbox_with_lineedit(items, items_per_row)
        self.main_layout.addWidget(groupbox)
        self.setLayout(self.main_layout)

    def create_groupbox_with_lineedit(self, items, items_per_row=1):
        """Create a group box with form layout for biometrics."""
        groupbox = QGroupBox("Biometrics")
        layout = QFormLayout()

        # Create QLineEdit for each item and add to the form layout
        for item in items:
            layout.addRow(QLabel(item), QLineEdit())

        groupbox.setLayout(layout)
        return groupbox
biometrics = ["Pulse", "Height", "Weight", "POX"]

# def open_biometric_window(self):
#     import subprocess
#     process = subprocess.Popen(["python", "C:\\Users\\user\\Documents\\QuickNotes2\\Objective\\biometrics.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     stdout, stderr = process.communicate()
#     if stdout:
#         print("Output:", stdout.decode())
#     if stderr:
#         print("Error:", stderr.decode())

# def open_observation_window(self):
#     import subprocess
#     process = subprocess.Popen(["python", "C:\\Users\\user\\Documents\\QuickNotes2\\Objective\\biometrics.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     stdout, stderr = process.communicate()
#     if stdout:
#         print("Output:", stdout.decode())
#     if stderr:
#         print("Error:", stderr.decode())