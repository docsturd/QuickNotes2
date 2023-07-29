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
            ["neck pain", "upper back pain", "low back pain", "headache",
             "shoulder pain Right", "shoulder pain Left",
             "hip pain Right", "hip pain Left",
             "Sciatica Right", "sciatica Left",
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

    # COMPLAINT
        complaint_label = QLabel("Complaint: ")
        hbox.addWidget(complaint_label)

        # create a dropdown list for symptoms
        symptoms_dropdown = QComboBox()
        symptoms_dropdown.setEditable(True)
        symptoms_dropdown = PlaceholderComboBox()
        symptoms_dropdown.setObjectName(title)  # Set object name as title to reference it later
        symptoms_dropdown.addItem("")
        symptoms_dropdown.addItems(symptoms)
        symptoms_dropdown.setFixedWidth(300)

        completer = QCompleter(symptoms)
        completer.setCaseSensitivity(False)
        symptoms_dropdown.setCompleter(completer)

        hbox.addWidget(symptoms_dropdown)

        # create label for Pain Severity
        pain_severity_label = QLabel("  Pain Severity: ")
        hbox.addWidget(pain_severity_label)

        # create radio button group for pain severity
        pain_severity_button_group = QButtonGroup()

        # Create and add the radio buttons to the layout and button group
        for i in range(10):
            pain_severity_radio_button = QRadioButton(str(i + 1))
            hbox.addWidget(pain_severity_radio_button)
            pain_severity_button_group.addButton(pain_severity_radio_button, i + 1)

        vbox.addLayout(hbox)  # add first hbox to vbox

        # Add a horizontal line
        hline = QFrame()
        hline.setFrameShape(QFrame.HLine)
        hline.setFrameShadow(QFrame.Sunken)
        vbox.addWidget(hline)

    # COMPLICATIONS
        # Add the title for the check boxes
        complications_title = QLabel("Complicated by")
        vbox.addWidget(complications_title)

        complications_list = ["arm numb Right", "Right",
                              "hand Right", "hand Right",
                              "severe pain", "diabetes", "alcohol", "autoimmune", "age", "degenerative changes",
                              "compliance", "work", "sedentary", "unrealistic expectations"]

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
        # Add a horizontal line
        hline2 = QFrame()
        hline2.setFrameShape(QFrame.HLine)
        hline2.setFrameShadow(QFrame.Sunken)
        vbox.addWidget(hline2)

    # HOW
        how_it_happened_title = QLabel("HOW DID IT HAPPEN:")
        self.how_it_happened_edit = QLineEdit()
        self.set_background_text(self.how_it_happened_edit, "Enter how it happened here...")

    # WHEN
        when_it_happened_title = QLabel("WHEN DID IT HAPPEN:")
        self.when_it_happened_edit = QLineEdit()
        self.when_it_happened_edit.setFixedWidth(85)
        validator = QIntValidator(0, 9999)  # To make sure only integers are entered
        self.when_it_happened_edit.setValidator(validator)
        self.set_background_text(self.when_it_happened_edit, "# DWMY...")

        # Create a radio button group for time periods
        self.time_period_button_group = QButtonGroup()
        time_periods = ["today", "yesterday", "days", "weeks", "months", "years"]
        hbox_time_periods = QHBoxLayout()

        for i, period in enumerate(time_periods):
            time_period_radio_button = QRadioButton(period)
            hbox_time_periods.addWidget(time_period_radio_button)
            self.time_period_button_group.addButton(time_period_radio_button, i + 1)

        # Add "HOW DID IT HAPPEN", "WHEN DID IT HAPPEN", and time periods to the same row
        hbox_how_and_when_it_happened = QHBoxLayout()
        hbox_how_and_when_it_happened.addWidget(how_it_happened_title)
        hbox_how_and_when_it_happened.addWidget(self.how_it_happened_edit)
        hbox_how_and_when_it_happened.addWidget(when_it_happened_title)
        hbox_how_and_when_it_happened.addWidget(self.when_it_happened_edit)
        hbox_how_and_when_it_happened.addLayout(hbox_time_periods)

        vbox.addLayout(hbox_how_and_when_it_happened)

        # Add a horizontal line
        hline3 = QFrame()
        hline3.setFrameShape(QFrame.HLine)
        hline3.setFrameShadow(QFrame.Sunken)
        vbox.addWidget(hline3)
    # TIMING opqrsT



        # BUTTONS
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

    def symptom_emit_text(self, symptom, pain_severity, title):
        if not symptom:  # if no symptom is selected from the QComboBox
            error_dialog = QMessageBox()
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setText("Error")
            error_dialog.setInformativeText("Please select a symptom from the dropdown menu.")
            error_dialog.setWindowTitle("Error")
            error_dialog.exec_()
            return

        # COMPLAINT
        group_specific_lambda = {
            "Chief Complaints": lambda: f"\nChief complaint: {symptom}.",
            "Secondary Complaint": lambda: f"\nSecondary: {symptom}.",
        }
        complaint_text = group_specific_lambda[title]()

        # COMPLICATED BY
        checked_complications = [comp for comp, checked in self.complications.items() if checked]
        if checked_complications:
            complication_text = ", ".join(checked_complications[:-1])
            if len(checked_complications) > 1:
                complication_text += f" and {checked_complications[-1]}"
            else:
                complication_text = checked_complications[0]
            complication_text = f" Complicated by: {complication_text}."
        else:
            complication_text = ""

        # SEVERITY
        if 1 <= pain_severity <= 10:
            severity_lambda = lambda severity: f"Pain on VAS: {severity}/10."
            severity_text = severity_lambda(pain_severity)  # Call the lambda function for pain severity
        else:
            severity_text = ""

        # HOW
        how_it_happened_text = self.how_it_happened_edit.text().strip()
        if how_it_happened_text:
            how_it_happened_text = f"\nHow it happened: {how_it_happened_text}."
        else:
            how_it_happened_text = ""

        # WHEN
        # Add this to get the text from the "WHEN DID IT HAPPEN" QLineEdit
        when_it_happened_number = self.when_it_happened_edit.text().strip()
        selected_radio_button = self.time_period_button_group.checkedButton()

        if selected_radio_button is not None:  # if a button is selected
            when_it_happened_period = selected_radio_button.text().lower()
        else:
            when_it_happened_period = ""  # or set a default value

        # If the selected period is "today" or "yesterday", no number is included.
        if when_it_happened_period in ['today', 'yesterday']:
            when_it_happened_text = f"\nWhen it happened: {when_it_happened_period}."
        else:
            if not when_it_happened_number and when_it_happened_period in ["days", "weeks", "months", "years"]:
                error_dialog = QMessageBox()
                error_dialog.setIcon(QMessageBox.Critical)
                error_dialog.setText("Error")
                error_dialog.setInformativeText("Please enter a number for 'When did it happen?' field.")
                error_dialog.setWindowTitle("Error")
                error_dialog.exec_()
                return
            elif when_it_happened_number:
                when_it_happened_text = f"\nWhen it happened: {when_it_happened_number} {when_it_happened_period} ."
            else:
                when_it_happened_text = ""


        # Emit full text
        full_text = complaint_text + complication_text + '\n' + severity_text + how_it_happened_text + when_it_happened_text


        self.text_to_append.emit(full_text)

    def set_complication(self, complication, state):
        self.complications[complication] = state == Qt.Checked
    def set_background_text(self, qlineedit, text):
        qlineedit.setPlaceholderText(text)



#########  Add Primary , 2nd make Additionl complaint into checkbox
######### use a table pandas to put Chief Complaints", "Secondary Complaint", "Complicated By", "Additional Complaints  HEADERS
############ column OPQRST
class PlaceholderComboBox(QComboBox):
    def __init__(self, parent=None):
        super(PlaceholderComboBox, self).__init__(parent)
        self.setEditable(True)
        line_edit = QLineEdit()
        line_edit.setPlaceholderText("Search or Enter custom symptom here...")
        self.setLineEdit(line_edit)

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
