from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


#######################  Evaluate def create_group_box to simplify by removeing redunances



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
        self.qualities = {} # create a dictionary to store Qualities
        self.provocations = {} # create a dictionary to store provocations
        self.interfers_daily_living = {}

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
        symptoms_dropdown = PlaceholderComboBox("Search or Enter custom symptom here...")
        symptoms_dropdown.setObjectName(title)  # Set object name as title to reference it later
        symptoms_dropdown.addItem("")
        symptoms_dropdown.addItems(symptoms)
        symptoms_dropdown.setFixedWidth(300)

        completer = QCompleter(symptoms)
        completer.setCaseSensitivity(False)
        symptoms_dropdown.setCompleter(completer)

        hbox.addWidget(symptoms_dropdown)

        # Severity
        pain_severity_label = QLabel(f"\tPain Severity: ")
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
        hline0 = QFrame()
        hline0.setFrameShape(QFrame.HLine)
        hline0.setFrameShadow(QFrame.Sunken)
        vbox.addWidget(hline0)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox.addItem(spacer)

# RADICULAR, PERCENT, BETTER WORSE,
        # Create QComboBox for "Is Pain Radicular?:" Right Shoulder, Left shoulder
        radicular = ["shoulder Right ", "shoulder Left", "hand digits 3,4,5 Right", "hand digits 3,4,5 Left",
        "hand digits 1,2 Right", "hand digits 1,2 Left"]
        pain_radicular_label = QLabel("Is Pain Radicular?:")

        self.pain_radicular_combo = QComboBox()
        # self.set_background_text(self.pain_radicular_combo, "Search or Enter custom radicular sx ...")
        self.pain_radicular_combo.setEditable(True)
        self.pain_radicular_combo = PlaceholderComboBox("Search or Enter custom radicular sx ...")
        self.pain_radicular_combo.addItem("")
        self.pain_radicular_combo.addItems(radicular)
        self.pain_radicular_combo.setFixedWidth(300)
        completer = QCompleter(radicular)
        completer.setCaseSensitivity(False)
        self.pain_radicular_combo.setCompleter(completer)

        pain_percentage_label = QLabel(f"\t% of 24hour you feel pain:")
        self.pain_percentage_edit = QLineEdit()
        self.pain_percentage_edit.setFixedWidth(80)
        self.set_background_text(self.pain_percentage_edit, "# 1-100")

        # Create QRadioButtons for {improved, worse, no change, 1st visit}
        pain_status_label = QLabel(f"\tPain status:")
        self.pain_status_improved_rb = QRadioButton("Improved")
        self.pain_status_worse_rb = QRadioButton("Worse")
        self.pain_status_no_change_rb = QRadioButton("No Change")
        self.pain_status_1st_visit_rb = QRadioButton("1st visit")

        # Create a QHBoxLayout to add all widgets
        hbox_percent_better_worse_radicular = QHBoxLayout()
        hbox_percent_better_worse_radicular.addWidget(pain_radicular_label)
        hbox_percent_better_worse_radicular.addWidget(self.pain_radicular_combo)
        hbox_percent_better_worse_radicular.addWidget(pain_percentage_label)
        hbox_percent_better_worse_radicular.addWidget(self.pain_percentage_edit)
        hbox_percent_better_worse_radicular.addWidget(pain_status_label)
        hbox_percent_better_worse_radicular.addWidget(self.pain_status_improved_rb)
        hbox_percent_better_worse_radicular.addWidget(self.pain_status_worse_rb)
        hbox_percent_better_worse_radicular.addWidget(self.pain_status_no_change_rb)
        hbox_percent_better_worse_radicular.addWidget(self.pain_status_1st_visit_rb)
        vbox.addLayout(hbox_percent_better_worse_radicular)

        # Add a horizontal line
        hline1 = QFrame()
        hline1.setFrameShape(QFrame.HLine)
        hline1.setFrameShadow(QFrame.Sunken)
        vbox.addWidget(hline1)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox.addItem(spacer)

# HOW
        how_it_happened_title = QLabel("How did it happen:")
        self.how_it_happened_edit = QLineEdit()
        # self.set_background_text(self.how_it_happened_edit, "Enter how it happened here...")

# WHEN
        when_it_happened_title = QLabel("When did it happen:")
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
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox.addItem(spacer)

# QUALITY
        # Add the title for the check boxes
        qualities_title = QLabel("Quality")
        vbox.addWidget(qualities_title)

        qualities_list = quality_list = ["Sharp", "Shooting", "Sharp", "Dull", "Burning", "tingling", "Numbness", "Throbbing", "Stabbing", "Aching", "Cramping", "Stiffness", "Swelling", "Radiating"]
        qualities_list = [quality.lower() for quality in qualities_list]
        # Sort the list alphabetically
        qualities_list.sort()

        MAX_ITEMS_PER_ROW = 7
        item_counter = 0
        hbox_qualities = QHBoxLayout()

        for quality in qualities_list:
            if item_counter >= MAX_ITEMS_PER_ROW:
                vbox.addLayout(hbox_qualities)
                hbox_qualities = QHBoxLayout()
                item_counter = 0

            checkbox = QCheckBox(quality)
            checkbox.stateChanged.connect(lambda state, checkbox=checkbox: self.set_quality(checkbox.text(), state))
            hbox_qualities.addWidget(checkbox)
            item_counter += 1

        if hbox_qualities.count() > 0:  # add remaining checkboxes if any
            vbox.addLayout(hbox_qualities)

        # Add a horizontal line
        hline1 = QFrame()
        hline1.setFrameShape(QFrame.HLine)
        hline1.setFrameShadow(QFrame.Sunken)
        vbox.addWidget(hline1)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox.addItem(spacer)

# PROVOITIVE
        # Add the title for the check boxes
        provocations_title = QLabel("provocative")
        vbox.addWidget(provocations_title)

        provocations_list = ["Sitting", "Bending", "Standing", "Lying down", "Walking", "Lifting"]
        provocations_list = [provocative.lower() for provocative in provocations_list]
        # Sort the list alphabetically
        provocations_list.sort()

        MAX_ITEMS_PER_ROW = 7
        item_counter = 0
        hbox_provocations = QHBoxLayout()

        for provocative in provocations_list:
            if item_counter >= MAX_ITEMS_PER_ROW:
                vbox.addLayout(hbox_provocations)
                hbox_provocations = QHBoxLayout()
                item_counter = 0

            checkbox = QCheckBox(provocative)
            checkbox.stateChanged.connect(lambda state, checkbox=checkbox: self.set_provocative(checkbox.text(), state))
            hbox_provocations.addWidget(checkbox)
            item_counter += 1

        if hbox_provocations.count() > 0:  # add remaining checkboxes if any
            vbox.addLayout(hbox_provocations)

        hline1 = QFrame()
        hline1.setFrameShape(QFrame.HLine)
        hline1.setFrameShadow(QFrame.Sunken)
        vbox.addWidget(hline1)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox.addItem(spacer)

# INTERFERS
        # Add the title for the check boxes
        interfers_daily_living_title = QLabel("interfer_daily_living")
        vbox.addWidget(interfers_daily_living_title)

        interfers_daily_living_list = ["Bathing", "Tolileting", "Preparing food", "Eating", "Walking", "Exercising", "Sleeping", "Dressing", "Tying Shoes", "Work performance"]
        interfers_daily_living_list = [interfer_daily_living.lower() for interfer_daily_living in interfers_daily_living_list]
        # Sort the list alphabetically
        interfers_daily_living_list.sort()

        MAX_ITEMS_PER_ROW = 10
        item_counter = 0
        hbox_interfers_daily_living = QHBoxLayout()

        for interfer_daily_living in interfers_daily_living_list:
            if item_counter >= MAX_ITEMS_PER_ROW:
                vbox.addLayout(hbox_interfers_daily_living)
                hbox_interfers_daily_living = QHBoxLayout()
                item_counter = 0

            checkbox = QCheckBox(interfer_daily_living)
            checkbox.stateChanged.connect(lambda state, checkbox=checkbox: self.set_interfer_daily_living(checkbox.text(), state))
            hbox_interfers_daily_living.addWidget(checkbox)
            item_counter += 1

        if hbox_interfers_daily_living.count() > 0:  # add remaining checkboxes if any
            vbox.addLayout(hbox_interfers_daily_living)

        hline1 = QFrame()
        hline1.setFrameShape(QFrame.HLine)
        hline1.setFrameShadow(QFrame.Sunken)
        vbox.addWidget(hline1)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox.addItem(spacer)
# COMPLICATIONS
        # Add the title for the check boxes
        complications_title = QLabel("Complicated by")
        vbox.addWidget(complications_title)

        complications_list = ["severe pain", "diabetes", "alcohol", "autoimmune", "age", "degenerative changes",
                              "compliance", "work", "sedentary", "unrealistic expectations"]
        # Sort the list alphabetically
        complications_list.sort()

        MAX_ITEMS_PER_ROW = 10
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
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox.addItem(spacer)

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

# SEVERITY
        if 1 <= pain_severity <= 10:
            severity_lambda = lambda severity: f"Pain on VAS: {severity}/10."
            severity_text = severity_lambda(pain_severity)  # Call the lambda function for pain severity
        else:
            severity_text = ""
# QULITY
        checked_qualities = [comp for comp, checked in self.qualities.items() if checked]
        if checked_qualities:
            quality_text = ", ".join(checked_qualities[:-1])
            if len(checked_qualities) > 1:
                quality_text += f" and {checked_qualities[-1]}"
            else:
                quality_text = checked_qualities[0]
            quality_text = f"Quality of: {quality_text}."
        else:
            quality_text = ""

# PROVOCATIONS EMIT
        checked_provocations = [qual for qual, checked in self.provocations.items() if checked]
        if checked_provocations:
            provocative_text = ", ".join(checked_provocations[:-1])
            if len(checked_provocations) > 1:
                provocative_text += f" and {checked_provocations[-1]}"
            else:
                provocative_text = checked_provocations[0]
            provocative_text = f"provocative of: {provocative_text}."
        else:
            provocative_text = ""

# interfers_daily_living EMIT
        checked_interfers_daily_living = [qual for qual, checked in self.interfers_daily_living.items() if checked]
        if checked_interfers_daily_living:
            interfer_daily_living_text = ", ".join(checked_interfers_daily_living[:-1])
            if len(checked_interfers_daily_living) > 1:
                interfer_daily_living_text += f" and {checked_interfers_daily_living[-1]}"
            else:
                interfer_daily_living_text = checked_interfers_daily_living[0]
            interfer_daily_living_text = f"interfer_daily_living of: {interfer_daily_living_text}."
        else:
            interfer_daily_living_text = ""

# RADICULAR
        radicular_pain_text = self.pain_radicular_combo.currentText().strip()
        if radicular_pain_text:
            radicular_pain_text = f"Radicular Pain Location: {radicular_pain_text}."
        else:
            radicular_pain_text = ""

# PAIN PERCENTAGE
        Time_percentOfDay = self.pain_percentage_edit.text().strip()
        if Time_percentOfDay:
            Time_percentOfDay = f"Time : {Time_percentOfDay}% of day."
        else:
            Time_percentOfDay = ""

# PAIN STATUS
        pain_status_text = ""
        if self.pain_status_improved_rb.isChecked():
            pain_status_text = "Pain Status: Improved."
        elif self.pain_status_worse_rb.isChecked():
            pain_status_text = "Pain Status: Worsened."
        elif self.pain_status_no_change_rb.isChecked():
            pain_status_text = "Pain Status: No change."
        elif self.pain_status_1st_visit_rb.isChecked():
            pain_status_text = "Pain Status: First visit."


# COMPLICATED BY
        checked_complications = [comp for comp, checked in self.complications.items() if checked]
        if checked_complications:
            complication_text = ", ".join(checked_complications[:-1])
            if len(checked_complications) > 1:
                complication_text += f" and {checked_complications[-1]}"
            else:
                complication_text = checked_complications[0]
            complication_text = f"Complicated by: {complication_text}."
        else:
            complication_text = ""

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

#MISSING TEXT
        # Emit full text
        full_text = complaint_text + '\n' + complication_text + '\n' + quality_text + '\n' + provocative_text + '\n' + interfer_daily_living_text + '\n' + severity_text + how_it_happened_text + when_it_happened_text + '\n' + radicular_pain_text + '\n' + Time_percentOfDay + '\n' + pain_status_text


        self.text_to_append.emit(full_text)

    def set_quality(self, quality, state):
        self.qualities[quality] = state == Qt.Checked
    def set_provocative(self, provocative, state):
        self.provocations[provocative] = state == Qt.Checked
    def set_interfer_daily_living(self, interfer_daily_living, state):
        self.interfers_daily_living[interfer_daily_living] = state == Qt.Checked
    def set_complication(self, complication, state):
        self.complications[complication] = state == Qt.Checked


    def set_background_text(self, qlineedit, text):
        qlineedit.setPlaceholderText(text)





#########  Add Primary , 2nd make Additionl complaint into checkbox
######### use a table pandas to put Chief Complaints", "Secondary Complaint", "Complicated By", "Additional Complaints  HEADERS
############ column OPQRST

class PlaceholderComboBox(QComboBox):
    def __init__(self, placeholder_text, parent=None):
        super(PlaceholderComboBox, self).__init__(parent)
        self.setEditable(True)
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder_text)
        self.setLineEdit(line_edit)
        ###########USAGE################
        # combo_box = PlaceholderComboBox("Search or Enter custom symptom here...")
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
class CustomDropDownTEST:
    def __init__(self, title, symptoms, label_text, width=300):
        self.hbox = QHBoxLayout()

        complaint_label = QLabel(label_text)  # Set label text from parameter
        self.hbox.addWidget(complaint_label)

        # create a dropdown list for symptoms
        self.dropdown = QComboBox()
        self.dropdown.setEditable(True)
        self.dropdown.setObjectName(title)  # Set object name as title to reference it later
        self.dropdown.addItem("")
        self.dropdown.addItems(symptoms)
        self.dropdown.setFixedWidth(width)

        completer = QCompleter(symptoms)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.dropdown.setCompleter(completer)

        self.hbox.addWidget(self.dropdown)

    def get_layout(self):
        return self.hbox

    def get_dropdown(self):
        return self.dropdown

    ##################USAGE###################
    # title = "dropdown_title"
    # symptoms_list = ["symptom1", "symptom2", "symptom3"]
    # label_text = "Complaint: "
    #
    # dropdown = CustomDropDown(title, symptoms_list, label_text)
    # layout.addLayout(dropdown.get_layout())
