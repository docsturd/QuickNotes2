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
        group_box_titles = ["Chief Complaints"]

        # Corresponding list of symptoms for each group box
        symptoms = [
            ["neck pain", "upper back pain", "low back pain", "Headache",
             "Shoulder pain Right", "Shoulder pain Left",
             "Hip Pain Right", "Hip Pain Left",
             "Sciatica Right", "Sciatica Left",
             "TMJ Right", "TMJ Left"]
        ]

        self.complications = {}  # create a dictionary to store complications

        for title, symptom_list in zip(group_box_titles, symptoms):
            layout.addWidget(self.create_group_box(title, symptom_list))
            layout.addSpacing(20)  # add space between group boxes
        # Add a stretch to push all content to the top
        layout.addStretch(1)
        self.setLayout(layout)

    def create_group_box(self, title, symptoms):
        groupBox = QGroupBox(title)  # Create a QGroupBox
        vbox = QVBoxLayout()  # Create a layout for the group box
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
            pain_severity_radio_button = QRadioButton(str(i + 1))
            hbox.addWidget(pain_severity_radio_button)
            pain_severity_button_group.addButton(pain_severity_radio_button, i + 1)

        # # Add a button to end of Hbox that appends all selected value in that groupbox
        # append_button_primary = QPushButton("Append Primary Complaint")
        # append_button_primary.clicked.connect(
        #     lambda: self.symptom_emit_text(symptoms_dropdown.currentText(), pain_severity_button_group.checkedId(),
        #                                    "Chief Complaints"))
        # hbox.addWidget(append_button_primary)
        #
        # append_button_secondary = QPushButton("Append Secondary Complaint")
        # append_button_secondary.clicked.connect(
        #     lambda: self.symptom_emit_text(symptoms_dropdown.currentText(), pain_severity_button_group.checkedId(),
        #                                    "Secondary Complaint"))
        # hbox.addWidget(append_button_secondary)

        vbox.addLayout(hbox)  # add first hbox to vbox

        # Add a horizontal line
        hline = QFrame()
        hline.setFrameShape(QFrame.HLine)
        hline.setFrameShadow(QFrame.Sunken)
        vbox.addWidget(hline)

        # Add the title for the check boxes
        complications_title = QLabel("Complicated by")
        vbox.addWidget(complications_title)

        # Complications checkboxes
        complications_list = ["arm Right", "Arm Right",
                              "hand Right", "hand Right",
                              "Severe pain", "Diabetes", "Alcohol", "Autoimmune", "Age", "degenerative changes",
                              "Compliance", "work", "Sedentary", "Unrealistic expectations"]

        MAX_ITEMS_PER_ROW = 7
        item_counter = 0
        hbox_complications = QHBoxLayout()

        for complication in complications_list:
            if item_counter >= MAX_ITEMS_PER_ROW:
                vbox.addLayout(hbox_complications)
                hbox_complications = QHBoxLayout()
                item_counter = 0

            checkbox = QCheckBox(complication)
            checkbox.stateChanged.connect(lambda state, checkbox=checkbox: self.set_complication(checkbox.text(), state))
            hbox_complications.addWidget(checkbox)
            item_counter += 1

        if hbox_complications.count() > 0:  # add remaining checkboxes if any
            vbox.addLayout(hbox_complications)

        # Adding the buttons
        hbox_buttons = QHBoxLayout()
        hbox_buttons.addStretch(1)  # This will push buttons to the right

        # Create Append Chief Complaint button
        append_chief_complaint_button = QPushButton("Append Chief Complaint")
        append_chief_complaint_button.clicked.connect(
            lambda: self.symptom_emit_text(symptoms_dropdown.currentText(), pain_severity_button_group.checkedId(), "Chief Complaints"))
        hbox_buttons.addWidget(append_chief_complaint_button)

        # Create Append Secondary Complaint button
        append_secondary_complaint_button = QPushButton("Append Secondary Complaint")
        append_secondary_complaint_button.clicked.connect(
            lambda: self.symptom_emit_text(symptoms_dropdown.currentText(), pain_severity_button_group.checkedId(), "Secondary Complaint"))
        hbox_buttons.addWidget(append_secondary_complaint_button)

        vbox.addLayout(hbox_buttons)

        groupBox.setLayout(vbox)

        return groupBox


    def emit_text_to_append(self, text):
        self.text_to_append.emit(text)

    def symptom_emit_text(self, symptom, pain_severity, title):
        group_specific_lambda = {
            "Chief Complaints": lambda: self.emit_text_to_append(f"\nChief complaint of symptom: {symptom}."),
            "Secondary Complaint": lambda: self.emit_text_to_append(f"\nSecondary complaint of symptom: {symptom}."),
        }
        group_specific_lambda[title]()
        if 1 <= pain_severity <= 10:
            severity_lambda = lambda severity: self.emit_text_to_append(
                f"Pain Severity on a 1-10 scale is {severity}/10.")
            severity_lambda(pain_severity)  # Call the lambda function for pain severity

        # Emit complication text
        checked_complications = [comp for comp, checked in self.complications.items() if checked]
        if checked_complications:
            complication_text = ", ".join(checked_complications[:-1])
            if len(checked_complications) > 1:
                complication_text += f" and {checked_complications[-1]}"
            else:
                complication_text = checked_complications[0]
            self.emit_text_to_append(f"Complicated by {complication_text}.")

    def set_complication(self, complication, state):
        self.complications[complication] = state == Qt.Checked



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
