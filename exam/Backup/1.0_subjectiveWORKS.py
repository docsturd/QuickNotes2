from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
#from PyQt5.QtPrintSupport import *
#from qt_material import *
#import qtawesome as qta

class Subjective(QWidget):
    text_to_append = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Subjective, self).__init__(parent)
        layout = QVBoxLayout(self)

        # List of group box titles
        group_box_titles = ["Chief Complaints", "Secondary Complaint", "Complicated By", "Additional Complaints"]

        # Corresponding list of symptoms for each group box
        symptoms = [
            ["neck pain", "upper back pain", "low back pain", "Headache",
            "Shoulder pain Right", "Shoulder pain Left",
            "Hip Pain Right", "Hip Pain  Left",
            "Sciatica Right", "Sciatica Left",
            "TMJ Right", "TMJ Left"],
            ["neck pain", "upper back pain", "low back pain", "Headache", "Shoulder pain", "Hip Pain", "Sciatica", "TMJ"],
            ["arm Right", "Arm Right",
            "hand Right", "hand Right",
            "Severe pain", "Diabetes", "Alcohol", "Autoimmune", "Age", "degenerative changes", "Compliance", "work", "Sedentary", "Unrealistic expectations"],
            ["nausea", "vomiting", "diarrhea", "abdominal pain", "cramping", "gas", "constipation", "indigestion"]
        ]

        for title, symptom_list in zip(group_box_titles, symptoms):
            layout.addWidget(self.create_group_box(title, symptom_list))
            layout.addSpacing(20)  # add space between group boxes
        # Add a stretch to push all content to the top
        layout.addStretch(1)
        self.setLayout(layout)

    def create_group_box(self, title, symptoms):
        groupBox = QGroupBox(title)  # Create a QGroupBox
        vbox = QVBoxLayout()  # Create a layout for the group box
        # # Create a horizontal box layout for dropdown list
        # hbox = QHBoxLayout()

        if title in ["Chief Complaints", "Secondary Complaint"]:
            hbox = QHBoxLayout()
            # create label and line edit
            complaint_label = QLabel("Complaint: ")
            hbox.addWidget(complaint_label)

            # create a dropdown list for symptoms
            symptoms_dropdown = QComboBox()
            symptoms_dropdown.setEditable(True)
            symptoms_dropdown.setObjectName(title)  # Set object name as title to reference it later
            symptoms_dropdown.addItem("")
            symptoms_dropdown.addItems(symptoms)
            completer = QCompleter(symptoms)
            completer.setCaseSensitivity(False)
            symptoms_dropdown.setCompleter(completer)

            hbox.addWidget(symptoms_dropdown)

            # create label for Pain Severity
            pain_severity_label = QLabel("Pain Severity on a 1-10 scale is: ")
            hbox.addWidget(pain_severity_label)

           # create radio button group for pain severity
            pain_severity_button_group = QButtonGroup()

            # Create and add the radio buttons to the layout and button group
            for i in range(10):
                pain_severity_radio_button = QRadioButton(str(i+1))
                hbox.addWidget(pain_severity_radio_button)
                pain_severity_button_group.addButton(pain_severity_radio_button, i+1)

            # Add a button to end of Hbox that appends all selected value in that groupbox
            append_button = QPushButton("Append Text")
            append_button.clicked.connect(
                lambda: self.symptom_emit_text(symptoms_dropdown.currentText(), pain_severity_button_group.checkedId(), title))
            hbox.addWidget(append_button)
            vbox.addLayout(hbox)

        elif title in ["Complicated By", "Additional Complaints"]:
            hbox = QHBoxLayout()
            checkbox_per_row = 10  # set the number of checkboxes per row
            counter = 0

            for symptom in symptoms:
                checkbox = QCheckBox(symptom)
                checkbox.stateChanged.connect(
                    lambda state, symptom=symptom: self.emit_text_to_append(
                        f"\n{title}: {symptom} {'checked' if state == Qt.Checked else 'unchecked'}.")
                )
                hbox.addWidget(checkbox)
                counter += 1
                if counter % checkbox_per_row == 0:
                    vbox.addLayout(hbox)
                    hbox = QHBoxLayout()
            vbox.addLayout(hbox)  # add remaining checkboxes if any

        groupBox.setLayout(vbox)

        return groupBox

    def emit_text_to_append(self, text):
        self.text_to_append.emit(text)

    def symptom_emit_text(self, symptom, pain_severity, title):
        group_specific_lambda = {
            "Chief Complaints": lambda: self.emit_text_to_append(f"\nChief complaint of symptom: {symptom}."),
            "Secondary Complaint": lambda: self.emit_text_to_append(f"\nSecondary complaint of {symptom}."),
            "Complicated By": lambda: self.emit_text_to_append(f"\nPatient patients condition is complicated by {symptom}."),
            "Additional Complaints": lambda: self.emit_text_to_append(f"\nAdditional complaints: " + symptom + '.  ')
        }
        group_specific_lambda[title]()
        if 1 <= pain_severity <= 10:
            severity_lambda = lambda severity: self.emit_text_to_append(f"Pain Severity on a 1-10 scale is {severity}/10.")
            severity_lambda(pain_severity)  # Call the lambda function for pain severity
        else:
            severity_lambda = None

#########  Add Primary , 2nd make Additionl complaint into checkbox
######### use a table pandas to put Chief Complaints", "Secondary Complaint", "Complicated By", "Additional Complaints  HEADERS
############ column OPQRST


class Subjective_POPUP(QDialog):
    def __init__(self, symptom, parent=None):
        super(Subjective_POPUP, self).__init__(parent)
        self.setWindowTitle('Subjective Popup')

        # Main vertical layout
        layout = QVBoxLayout(self)

        # Creating and styling the symptom label
        self.label = QLabel(symptom, self)
        self.label.setStyleSheet("font-size: 30px") # make the font size large
        layout.addWidget(self.label)

        # Create horizontal layout for the QLineEdit, QLabel, and radio buttons
        hbox = QHBoxLayout()

        # Create QLineEdit, and labels
        self.textBox = QLineEdit()
        label1 = QLabel("Complaint #1")
        label2 = QLabel("Pain Severity on a 1-10 scale is:")

        # Add QLineEdit and labels to the hbox layout
        hbox.addWidget(self.textBox)
        hbox.addWidget(label1)
        hbox.addWidget(label2)

        # Create 10 radio buttons and add them to the hbox layout
        self.radioButtons = []
        for i in range(1, 11):
            radioButton = QRadioButton(str(i))
            radioButton.toggled.connect(self.updateLabel)  # connect radioButton signal to updateLabel slot
            self.radioButtons.append(radioButton)
            hbox.addWidget(radioButton)

        # Add the hbox layout to the main layout
        layout.addLayout(hbox)

    def updateLabel(self):
        for i in range(10):
            if self.radioButtons[i].isChecked():
                self.label.setText(f"{self.label.text()} Pain severity on a 1-10 scale is: {i+1}")
                break
