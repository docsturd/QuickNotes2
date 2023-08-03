from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QFormLayout, QGroupBox

class BiometricWindow(QWidget):
    
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

if __name__ == '__main__':
    app = QApplication([])
    biometrics = ["Pulse", "Height", "Weight", "POX"]
    window = BiometricWindow(biometrics)
    window.show()
    app.exec_()
