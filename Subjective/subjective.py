from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import random
from utils.layout_tools import create_horizontal_line_with_spacer


class Subjective(QWidget):
    text_to_append = pyqtSignal(str)
    update_output =pyqtSignal(str)

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
        self.quality_checkboxes = []
        self.provocative_checkboxes = []
        self.interfers_checkboxes = []
        self.complications_checkboxes = []
        self.complications = {}  # create a dictionary to store complications
        self.qualities = {} # create a dictionary to store Qualities
        self.interfers = {}
        self.provocations = {} # create a dictionary to store provocations


        for title, symptom_list in zip(group_box_titles, symptoms):
            layout.addWidget(self.create_group_box(title, symptom_list))
            layout.addSpacing(20)  # add space between group boxes
        # Add a stretch to push all content to the top
        layout.addStretch(1)
        self.setLayout(layout)
        #rest of code

    def create_group_box(self, title, symptoms):
        groupBox = QGroupBox(title)
        vbox = QVBoxLayout()

        # Complaint Section
        complaint_layout, symptoms_dropdown, pain_severity_button_group = self.create_cheif_complaint_vas_section(title, symptoms)
        vbox.addLayout(complaint_layout)
        vbox.addLayout(create_horizontal_line_with_spacer())
        # Pain Details Section (Radicular, Percent, Better Worse)
        vbox.addLayout(self.create_radicular_percent_better_worse_section())
        vbox.addLayout(create_horizontal_line_with_spacer())
        # Add the 'How' and 'When' section below
        vbox.addLayout(self.create_how_and_when_section())
        vbox.addLayout(create_horizontal_line_with_spacer())

        # HORIZONTAL BOX QUALITY, PROVOCITIVE, INTERFERS, COMPLICATIONS
        main_hbox = self.create_main_horizontal_quality_provocitive_interfers_complication_section()
        vbox.addLayout(main_hbox)

        # BUTTONS
        vbox.addLayout(self.create_buttons_chief_complaint_secondary_complaint_section(symptoms_dropdown, pain_severity_button_group))


        groupBox.setLayout(vbox)
        return groupBox

    def create_cheif_complaint_vas_section(self, title, symptoms):
        hbox = QHBoxLayout()

        # Existing code where you create symptoms_dropdown and other elements
        self.symptoms_dropdown = QComboBox()
        self.symptoms_dropdown.addItems(symptoms)
        # hbox.addWidget(self.symptoms_dropdown)

        pain_severity_button_group = QButtonGroup()

        # Complaint Label
        complaint_label = QLabel("Complaint: ")
        hbox.addWidget(complaint_label)

        # Dropdown for symptoms
        self.symptoms_dropdown = PlaceholderComboBox("Search or Enter custom symptom here...")
        self.symptoms_dropdown.setObjectName(title)
        self.symptoms_dropdown.addItem("")
        self.symptoms_dropdown.addItems(symptoms)
        self.symptoms_dropdown.setFixedWidth(300)
        completer = QCompleter(symptoms)
        completer.setCaseSensitivity(False)
        self.symptoms_dropdown.setCompleter(completer)
        hbox.addWidget(self.symptoms_dropdown)

        # Pain Severity Label
        pain_severity_label = QLabel(f"\tPain Severity: ")
        hbox.addWidget(pain_severity_label)
        # Radio button group for pain severity
        self.pain_severity_button_group = QButtonGroup()

        for i in range(10):
            pain_severity_radio_button = QRadioButton(str(i + 1))
            hbox.addWidget(pain_severity_radio_button)
            self.pain_severity_button_group.addButton(pain_severity_radio_button, i + 1)

        # return hbox
        return hbox, self.symptoms_dropdown, self.pain_severity_button_group

    def create_radicular_percent_better_worse_section(self):
        # RADICULAR, PERCENT, BETTER WORSE
        radicular = ["shoulder Right ", "shoulder Left", "hand digits 3,4,5 Right", "hand digits 3,4,5 Left",
                     "hand digits 1,2 Right", "hand digits 1,2 Left"]
        pain_radicular_label = QLabel("Is Pain Radicular?:")

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
        validator = QIntValidator(0, 100)         # Set the validator to accept integers in the range 1-100
        self.pain_percentage_edit.setValidator(validator)

        # RadioButtons for {improved, worse, no change, 1st visit}
        pain_status_label = QLabel(f"\tPain status:")
        self.pain_status_improved_rb = QRadioButton("Improved")
        self.pain_status_worse_rb = QRadioButton("Worse")
        self.pain_status_no_change_rb = QRadioButton("No Change")
        self.pain_status_1st_visit_rb = QRadioButton("1st visit")

        # Layout for this section
        hbox = QHBoxLayout()
        hbox.addWidget(pain_radicular_label)
        hbox.addWidget(self.pain_radicular_combo)
        hbox.addWidget(pain_percentage_label)
        hbox.addWidget(self.pain_percentage_edit)
        hbox.addWidget(pain_status_label)
        hbox.addWidget(self.pain_status_improved_rb)
        hbox.addWidget(self.pain_status_worse_rb)
        hbox.addWidget(self.pain_status_no_change_rb)
        hbox.addWidget(self.pain_status_1st_visit_rb)

        return hbox

    def create_how_and_when_section(self):
        # HOW
        how_it_happened_title = QLabel("How did it happen:")
        self.how_it_happened_edit = QLineEdit()
        # self.set_background_text(self.how_it_happened_edit, "Enter how it happened here...")

        # WHEN
        when_it_happened_title = QLabel("When did it happen:")
        self.when_it_happened_edit = QLineEdit()
        self.when_it_happened_edit.setFixedWidth(85)
        self.set_background_text(self.when_it_happened_edit, "# DWMY...")
        validator_when = QIntValidator(0, 31)  # To make sure only integers are entered
        self.when_it_happened_edit.setValidator(validator_when)


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

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_how_and_when_it_happened)
        return vbox

    def create_checkboxes_section(self, title, items):
        vbox = QVBoxLayout()

        # Convert to lowercase and sort
        items = [item.lower() for item in items]
        items.sort()

        MAX_ITEMS_PER_ROW = 2
        item_counter = 0
        hbox = QHBoxLayout()

        # Lists to store checkboxes (Only initialize if they don't already exist)
        if not hasattr(self, 'quality_checkboxes'):
            self.quality_checkboxes = []
        if not hasattr(self, 'provocative_checkboxes'):
            self.provocative_checkboxes = []
        if not hasattr(self, 'interfers_checkboxes'):
            self.interfers_checkboxes = []
        if not hasattr(self, 'complications_checkboxes'):
            self.complications_checkboxes = []

        for item in items:
            if item_counter >= MAX_ITEMS_PER_ROW:
                vbox.addLayout(hbox)
                hbox = QHBoxLayout()
                item_counter = 0

            checkbox = QCheckBox(item)
            if title == "Quality":
                checkbox.stateChanged.connect(lambda state, checkbox=checkbox: self.set_quality(checkbox.text(), state))
                self.quality_checkboxes.append(checkbox)
            elif title == "Provocative":
                checkbox.stateChanged.connect(lambda state, checkbox=checkbox: self.set_provocative(checkbox.text(), state))
                self.provocative_checkboxes.append(checkbox)
            elif title == "Interfers":
                checkbox.stateChanged.connect(lambda state, checkbox=checkbox: self.set_interfers(checkbox.text(), state))
                self.interfers_checkboxes.append(checkbox)
            elif title == "Complications":
                checkbox.stateChanged.connect(lambda state, checkbox=checkbox: self.set_complications(checkbox.text(), state))
                self.complications_checkboxes.append(checkbox)

            hbox.addWidget(checkbox)
            item_counter += 1

        if hbox.count() > 0:  # add remaining checkboxes if any
            vbox.addLayout(hbox)

        return vbox

    def create_main_horizontal_quality_provocitive_interfers_complication_section(self):
        main_hbox = QHBoxLayout()

        # Add Quality and Provocative sections into main horizontal box
        quality_vbox = self.create_checkboxes_section("Quality", ["Sharp", "Shooting", "Sharp", "Dull", "Burning", "tingling",
                                                             "Numbness", "Throbbing", "Stabbing", "Aching", "Cramping",
                                                             "Stiffness", "Swelling", "Radiating"])

        provocative_vbox = self.create_checkboxes_section("Provocative", ["Bending", "Standing", "Walking", "Lying down",
                                                                "Twisting", "Reaching", "Pushing", "Pulling", "Lifting"])

        interfers_vbox = self.create_checkboxes_section("Interfers", ["Work", "Sleep", "Travel", "Bathing", "Tolileting",
                                                                "Preparing food", "Eating", "Walking", "Exercising", "Sleeping",
                                                                "Dressing", "Tying Shoes", "Work"])

        complications_vbox = self.create_checkboxes_section("Complications", ["severe pain", "diabetes", "alcohol", "autoimmune", "age",
                                                                "degeneration", "compliance", "work", "sedentary"])
        GROUPBOX_BETWEEN_PADDING = 50

        # Create group boxes to wrap the vbox layouts
        quality_groupbox = QGroupBox("Quality")
        quality_groupbox.setLayout(quality_vbox)

        provocative_groupbox = QGroupBox("Provocative")
        provocative_groupbox.setLayout(provocative_vbox)

        interfers_groupbox = QGroupBox("Interfers")
        interfers_groupbox.setLayout(interfers_vbox)

        complications_groupbox = QGroupBox("Complications")
        complications_groupbox.setLayout(complications_vbox)

        # Add the group boxes to the main horizontal layout
        main_hbox.addWidget(quality_groupbox)
        main_hbox.addSpacing(GROUPBOX_BETWEEN_PADDING)
        main_hbox.addWidget(provocative_groupbox)
        main_hbox.addSpacing(GROUPBOX_BETWEEN_PADDING)
        main_hbox.addWidget(interfers_groupbox)
        main_hbox.addSpacing(GROUPBOX_BETWEEN_PADDING)
        main_hbox.addWidget(complications_groupbox)

        return main_hbox

    def create_buttons_chief_complaint_secondary_complaint_section(self, symptoms_dropdown, pain_severity_button_group):
        hbox_buttons = QHBoxLayout()
        hbox_buttons.addStretch(1)  # This will push buttons to the right

        # Create Append Chief Complaint button
        append_chief_complaint_button = QPushButton("Chief Complaint")
        append_chief_complaint_button.clicked.connect(
            lambda: self.symptom_emit_text(symptoms_dropdown.currentText(), pain_severity_button_group.checkedId(), "Chief Complaints"))
        append_chief_complaint_button.clicked.connect(self.clear_all_fields)  # Clear fields when button is clicked
        hbox_buttons.addWidget(append_chief_complaint_button)

        # Create Append Secondary Complaint button
        append_secondary_complaint_button = QPushButton("Secondary Complaint")
        append_secondary_complaint_button.clicked.connect(
            lambda: self.symptom_emit_text(symptoms_dropdown.currentText(), pain_severity_button_group.checkedId(), "Secondary Complaint"))
        append_secondary_complaint_button.clicked.connect(self.clear_all_fields)  # Clear fields when button is clicked
        hbox_buttons.addWidget(append_secondary_complaint_button)

        return hbox_buttons

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
            "Chief Complaints": lambda: f"CC: {symptom.upper()}",
            "Secondary Complaint": lambda: f"Other Complaints {symptom.upper()}",
        }
        complaint_text = group_specific_lambda[title]()

# SEVERITY
        if 1 <= pain_severity <= 10:
            severity_lambda = lambda severity: f"VAS: {severity}/10     "
            severity_text = severity_lambda(pain_severity)  # Call the lambda function for pain severity
        else:
            severity_text = ""
# RADICULAR
        radicular_pain_text = self.pain_radicular_combo.currentText().strip()
        if radicular_pain_text:
            radicular_pain_text = f"RADIATES: {radicular_pain_text}     "
        else:
            radicular_pain_text = ""

# PAIN PERCENTAGE
        Time_percentOfDay = self.pain_percentage_edit.text().strip()
        if Time_percentOfDay:
            Time_percentOfDay = f"% OF DAY: {Time_percentOfDay}%     "
        else:
            Time_percentOfDay = ""

# PAIN STATUS
        pain_status_text = ""
        if self.pain_status_improved_rb.isChecked():
            pain_status_text = "STATUS: Improved     "
        elif self.pain_status_worse_rb.isChecked():
            pain_status_text = "STATUS: Worsened     "
        elif self.pain_status_no_change_rb.isChecked():
            pain_status_text = "STATUS: No change     "
        elif self.pain_status_1st_visit_rb.isChecked():
            pain_status_text = "STATUS: First visit     "

# HOW
        how_it_happened_text = self.how_it_happened_edit.text().strip()
        if how_it_happened_text:
            how_it_happened_text = f"HOW: \"{how_it_happened_text}\"     "
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
            when_it_happened_text = f"WHEN: {when_it_happened_period}     "
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
                when_it_happened_text = f"WHEN: {when_it_happened_number} {when_it_happened_period} ago     "
            else:
                when_it_happened_text = ""
# QULITY
        checked_qualities = [comp for comp, checked in self.qualities.items() if checked]
        if checked_qualities:
            quality_text = ", ".join(checked_qualities[:-1])
            if len(checked_qualities) > 1:
                quality_text += f" and {checked_qualities[-1]}"
            else:
                quality_text = checked_qualities[0]
            quality_text = f"QUALITY: {quality_text}\t"
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
            provocative_text = f"PROVOCITIVE: {provocative_text}"
        else:
            provocative_text = ""

# interfers_daily_living EMIT
        checked_interfers = [comp for comp, checked in self.interfers.items() if checked]
        if checked_interfers:
            interfer_text = ", ".join(checked_interfers[:-1])
            if len(checked_interfers) > 1:
                interfer_text += f" and {checked_interfers[-1]}"
            else:
                interfer_text = checked_interfers[0]
            interfer_text = f"INTERFERS: {interfer_text}"
        else:
            interfer_text = ""

# COMPLICATED BY
        checked_complications = [comp for comp, checked in self.complications.items() if checked]
        if checked_complications:
            complication_text = ", ".join(checked_complications[:-1])
            if len(checked_complications) > 1:
                complication_text += f" and {checked_complications[-1]}"
            else:
                complication_text = checked_complications[0]
            complication_text = f"COMPLICATED BY: {complication_text}\t"
        else:
            complication_text = ""

#MISSING TEXT
        # Emit full text
        full_text = "\n" + complaint_text + "\n"
        full_text += "     " + severity_text + radicular_pain_text + Time_percentOfDay + "\n"
        full_text += "     " + pain_status_text + how_it_happened_text + when_it_happened_text + "\n"
        full_text += "     " + quality_text + provocative_text + "\n"
        full_text += "     " + complication_text + interfer_text  + "\n"
        self.text_to_append.emit(full_text)

    def set_background_text(self, qlineedit, text):
        qlineedit.setPlaceholderText(text)

    def set_quality(self, quality, state):
        self.qualities[quality] = state == Qt.Checked
    def set_provocative(self, provocative, state):
        self.provocations[provocative] = state == Qt.Checked
    def set_interfers(self, interfer, state):
        self.interfers[interfer] = state == Qt.Checked
    def set_complications(self, complication, state):
        self.complications[complication] = state == Qt.Checked
    def clear_all_fields(self):
        # Clear symptoms_dropdown
        if hasattr(self, 'symptoms_dropdown'):
            self.symptoms_dropdown.setCurrentIndex(0)

        # Clear pain severity radio buttons
        self.pain_severity_button_group.setExclusive(False)
        for button in self.pain_severity_button_group.buttons():
            button.setChecked(False)
        self.pain_severity_button_group.setExclusive(True)

        # Clear radicular pain combo box
        self.pain_radicular_combo.setCurrentIndex(0)

        # Clear pain percentage edit
        self.pain_percentage_edit.clear()

        # Clear pain status radio buttons
        self.pain_status_improved_rb.setChecked(False)
        self.pain_status_worse_rb.setChecked(False)
        self.pain_status_no_change_rb.setChecked(False)
        self.pain_status_1st_visit_rb.setChecked(False)

        # Clear "How did it happen" edit
        self.how_it_happened_edit.clear()

        # Clear "When did it happen" edit and radio buttons
        self.when_it_happened_edit.clear()
        self.time_period_button_group.setExclusive(False)
        for button in self.time_period_button_group.buttons():
            button.setChecked(False)
        self.time_period_button_group.setExclusive(True)

        # Clear Quality checkboxes
        for checkbox in self.quality_checkboxes:
            checkbox.setChecked(False)

        # Clear Provocative checkboxes
        for checkbox in self.provocative_checkboxes:
            checkbox.setChecked(False)

        # Clear Interfers checkboxes
        for checkbox in self.interfers_checkboxes:
            checkbox.setChecked(False)

        # Clear Complications checkboxes
        for checkbox in self.complications_checkboxes:
            checkbox.setChecked(False)


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
