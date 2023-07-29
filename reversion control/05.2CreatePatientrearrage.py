import sys
import json
import os

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PyQt5.QtCore import *
from qt_material import *
import qtawesome as qta

class LookAtPatientRecord(QDialog):

    def __init__(self, parent=None):
        super(LookAtPatientRecord, self).__init__(parent)
        self.setWindowTitle("Look At Patient Record")

        # # Set the size of the popup window based on screen dimensions
        # screen_width = QApplication.desktop().screenGeometry().width()
        # screen_height = QApplication.desktop().screenGeometry().height()
        # # popup_width = int(screen_width * 0.6)  # Set the width to 60% of screen width
        # popup_height = int(screen_height * 0.6)  # Set the height to 60% of screen height
        # self.resize(screen_width, popup_height)

        # Create the label with large font
        label = QLabel("Patient Record this page should have open patient record with buttons for exam, soap, xray report")
        font = label.font()
        font.setPointSize(20)  # Set the font size to 20 points
        label.setFont(font)

        # Create the search input and radio buttons
        search_input = QLineEdit()
        search_input.setFixedWidth(150)  # Set the width to 150 pixels
        last_name_radio = QRadioButton("Search by Last Name")
        id_radio = QRadioButton("Search by ID")

        # Create a layout for the search input and radio buttons
        search_layout = QHBoxLayout()
        search_layout.addWidget(search_input)
        search_layout.addWidget(last_name_radio)
        search_layout.addWidget(id_radio)

        # Create a container widget to center the search layout
        search_container = QWidget()
        search_container.setLayout(search_layout)
        search_container_layout = QHBoxLayout()
        search_container_layout.addWidget(search_container)


        # Define the extremity names
        extremity_names = ['Add New Patient', 'Edit Patient', 'Delete Patient', 'New Patient Exams', 'Daily Soap Note', 'X-Ray Report', 'Forms', 'Femur', 'Tibia', 'Fibula', 'Talus', 'Calcaneus']

        # Create the button grid layout
        button_layout = QGridLayout()

        # Add buttons with names from the extremity_names list
        for i, extremity_name in enumerate(extremity_names):
            row = i % 3
            column = i // 3
            button = QPushButton(extremity_name)
            button.setFixedSize(200, 100)  # Set the button size
            button_layout.addWidget(button, row, column)
        # Set up the layout and add the label
        layout = QVBoxLayout()
        layout.addLayout(search_container_layout)
        layout.addWidget(label)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.exec()

class CreatePatientPopup(QDialog):

    def __init__(self, parent=None):
        super(CreatePatientPopup, self).__init__(parent)
        self.setWindowTitle("Create, Edit, Delete Patient")

        # Validators
        alphanumeric = QRegExp("[a-zA-Z0-9]+")
        validator = QRegExpValidator(alphanumeric)


        # Create input fields

        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.search_records)
        self.search_list = QListWidget()
        self.search_list.setFixedHeight(200)
        self.search_list.itemClicked.connect(self.populate_fields)

        self.first_name_input = QLineEdit()
        self.first_name_input.editingFinished.connect(self.generate_id)

        self.last_name_input = QLineEdit()
        self.last_name_input.editingFinished.connect(self.generate_id)

        self.date_of_birth_input = QDateEdit()
        self.date_of_birth_input.setCalendarPopup(True)
        self.date_of_birth_input.editingFinished.connect(self.generate_id)

        self.gender_input = QComboBox()
        self.gender_input.addItem("Male")
        self.gender_input.addItem("Female")

        self.id_input = QLineEdit()
        self.current_patient_id = None

        self.warning_input = QTextEdit()
        self.special_note_input = QTextEdit()

        # Create a layout for the input fields
        personal_details_layout = QFormLayout()
        personal_details_layout.addRow("First Name:", self.first_name_input)
        personal_details_layout.addRow("Last Name:", self.last_name_input)

        other_details_layout = QFormLayout()
        other_details_layout.addRow("Date of Birth:", self.date_of_birth_input)
        other_details_layout.addRow("Gender:", self.gender_input)
        other_details_layout.addRow("Warning:", self.warning_input)
        other_details_layout.addRow("Special Note:", self.special_note_input)
        other_details_layout.addRow("ID:", self.id_input)

        # Grouping
        personal_details_group = QGroupBox("Personal Details")
        personal_details_group.setLayout(personal_details_layout)

        other_details_group = QGroupBox("Other Details")
        other_details_group.setLayout(other_details_layout)

        # Create buttons for apply changes, save and cancel actions
        self.apply_button = QPushButton("Apply Changes")
        self.apply_button.clicked.connect(self.apply_changes)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save)

        self.delete_button = QPushButton("Delete Record")
        self.delete_button.clicked.connect(self.delete_record)
        self.delete_button.setEnabled(False)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)

        # Create a main layout for the dialog
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel("Search:"))
        main_layout.addWidget(self.search_input)
        main_layout.addWidget(self.search_list)
        main_layout.addWidget(personal_details_group)
        main_layout.addWidget(other_details_group)
        main_layout.addWidget(self.apply_button)
        main_layout.addWidget(save_button)
        main_layout.addWidget(self.delete_button)
        main_layout.addWidget(cancel_button)

        self.setLayout(main_layout)
        self.resize(800, self.height())  # set the width to 800px
        self.exec()

    def search_records(self):
        self.search_list.clear()
        query = self.search_input.text().lower()

        # Load existing patient data from the JSON file, if any
        existing_data = []
        try:
            with open("patients_names.json", "r") as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            pass

        # Find and display matches
        for patient in existing_data:
            first_name = patient.get('first_name', '').lower()
            last_name = patient.get('last_name', '').lower()
            patient_id = patient.get('patient_id', '')

            if patient_id is not None:
                patient_id = patient_id.lower()

            if query in first_name or query in last_name or query in patient_id:
                item = QListWidgetItem(patient['last_name'] + ', ' + patient['first_name'] + '\t   -   \t' + patient['patient_id'])
                item.setData(Qt.UserRole, patient)  # Store the full patient record with the list item
                self.search_list.addItem(item)
    def populate_fields(self, item):
        # Retrieve the patient data from the item
        patient = item.data(Qt.UserRole)
        # Update the current patient id
        self.current_patient_id = patient["patient_id"]

        # Assuming `patient` is a dict object with patient details.
        self.first_name_input.setText(patient["first_name"])
        self.last_name_input.setText(patient["last_name"])
        self.date_of_birth_input.setDate(QDate.fromString(patient["date_of_birth"], "MMddyyyy"))
        index = self.gender_input.findText(patient["gender"])
        self.gender_input.setCurrentIndex(index)
        self.id_input.setText(patient["patient_id"])
        self.warning_input.setText(patient["warning"])
        self.special_note_input.setText(patient["special_note"])

        self.delete_button.setEnabled(True)

    def delete_record(self):
        if self.current_patient_id is None:
            QMessageBox.warning(self, 'Warning', 'No patient selected.')
            return

        existing_data = []
        try:
            with open("patients_names.json", "r") as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            pass

        # Check if patient with the same ID exists
        existing_data = [pat for pat in existing_data if pat.get('patient_id') != self.current_patient_id]

        # Save the updated data to the JSON file
        with open("patients_names.json", "w") as file:
            json.dump(existing_data, file, indent=2)

        # Clear fields and search results
        self.clear_fields()
        self.search_records()  # This will now clear the search input field


    def apply_changes(self):
        # Get the values from the input fields
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        date_of_birth = self.date_of_birth_input.date().toString("MMddyyyy")
        gender = self.gender_input.currentText()
        warning = self.warning_input.toPlainText()
        special_note = self.special_note_input.toPlainText()

        # Generate patient id
        patient_id = self.id_input.text()

        # Create a dictionary object with the patient details
        patient = {
            "first_name": first_name,
            "last_name": last_name,
            "date_of_birth": date_of_birth,
            "gender": gender,
            "warning": warning,
            "special_note": special_note,
            "patient_id": patient_id
        }

        # Load existing patient data from the JSON file, if any
        existing_data = []
        try:
            with open("patients_names.json", "r") as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            pass

        # Check if patient with the same ID already exists
        for index, existing_patient in enumerate(existing_data):
            if existing_patient.get('patient_id') == self.current_patient_id:
                existing_data[index] = patient
                break
        else:
            # If no existing patient was found, add the new patient to the existing data
            existing_data.append(patient)

        # Save the updated data to the JSON file
        with open("patients_names.json", "w") as file:
            json.dump(existing_data, file, indent=2)

        # Clear the input fields and the current patient id
        self.clear_fields()
        self.current_patient_id = None
        self.search_input.clear()

    def clear_fields(self):
        self.first_name_input.clear()
        self.last_name_input.clear()
        self.date_of_birth_input.clear()
        self.gender_input.setCurrentIndex(0)
        self.id_input.clear()
        self.warning_input.clear()
        self.special_note_input.clear()
        self.search_input.clear()
        self.current_patient_id = None  # Clear current patient id
        self.delete_button.setEnabled(False)  # Disable the delete button


    def generate_id(self):

        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        date_of_birth = self.date_of_birth_input.date().toString("MMddyyyy")

        first_initial = first_name[0].upper() if first_name else ''
        last_initial = last_name[0].upper() if last_name else ''

        patient_id = date_of_birth + last_initial + first_initial
        self.id_input.setText(patient_id)

    def data_was_saved_successfully(self, patient_id):
        # Check if the patient record was saved by checking if it exists in the saved data
        try:
            with open("patients_names.json", "r") as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            return False

        if any(pat.get('patient_id') == patient_id for pat in existing_data):
            return True

        return False

    def save(self):
        # Get the values from the input fields
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        date_of_birth = self.date_of_birth_input.date().toString("MMddyyyy")
        gender = self.gender_input.currentText()
        warning = self.warning_input.toPlainText()
        special_note = self.special_note_input.toPlainText()

        # Generate patient id
        patient_id = self.id_input.text()

        # Create a dictionary object with the patient details
        patient = {
            "first_name": first_name,
            "last_name": last_name,
            "date_of_birth": date_of_birth,
            "gender": gender,
            "warning": warning,
            "special_note": special_note,
            "patient_id": patient_id
        }

        # Load existing patient data from the JSON file, if any
        existing_data = []
        try:
            with open("patients_names.json", "r") as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            pass

        if not self.current_patient_id:  # Only add a new patient if there is no current patient id
            # Check if patient with the same ID already exists
            if any(pat.get('patient_id') == patient_id for pat in existing_data):
                # Generate a unique identifier and append it to the ID
                unique_id = len(existing_data) + 1
                patient_id += str(unique_id)
                self.id_input.setText(patient_id)
                patient["patient_id"] = patient_id
                QMessageBox.warning(self, 'Warning', 'A patient with the initial ID already exists. A unique identifier has been appended to the ID.')

            # Add the new patient to the existing data
            existing_data.append(patient)

        else:
            # If there is a current patient id, just apply changes to the existing record
            for index, existing_patient in enumerate(existing_data):
                if existing_patient.get('patient_id') == self.current_patient_id:
                    existing_data[index] = patient
                    break

        # Save the updated data to the JSON file
        with open("patients_names.json", "w") as file:
            json.dump(existing_data, file, indent=2)

        # Clear the input fields and the current patient id
        self.clear_fields()
        self.current_patient_id = None
        self.search_input.clear()



class SettingsPopup(QDialog):
    def __init__(self, parent=None):
        super(SettingsPopup, self).__init__(parent)
        self.setWindowTitle("Practice Settings")

        self.load_settings()

# THEME
        self.theme_label = QLabel("Theme:")
        self.theme_dropdown = QComboBox()
        for theme in list_themes():
            self.theme_dropdown.addItem(theme)

        current_theme = self.prefs.get("theme", "")
        index = self.theme_dropdown.findText(current_theme)
        if index >= 0:
            self.theme_dropdown.setCurrentIndex(index)
    # helper question mark for theme
        self.theme_help_icon = qta.icon("fa.question-circle", color="gray")

        self.theme_help_label = QLabel()
        self.theme_help_label.setPixmap(self.theme_help_icon.pixmap(32, 32))
        self.theme_help_label.setToolTip("Theme will update next time program opens!")

        theme_layout = QHBoxLayout()
        theme_layout.addWidget(self.theme_dropdown)
        theme_layout.addWidget(self.theme_help_label)

# BUSSINESS NAME
        self.business_label = QLabel("Business Info:")
        self.business_input = QLineEdit()
        self.business_input.setText(self.prefs.get("business_info", ""))

# LOGO
        self.image_label = QLabel("Business Logo:")
        self.image_field = QLineEdit()
        self.image_field.setText(self.prefs.get("business_logo", ""))

        self.image_button = QPushButton("Select Business Logo")
        self.image_button.clicked.connect(self.select_image)

# ADDRESS
        self.address_label = QLabel("Business Address:")
        self.address_input = QLineEdit()
        self.address_input.setText(self.prefs.get("business_address", ""))

# CITY, STATE, ZIP
        self.city_label = QLabel("City:")
        self.city_input = QLineEdit()
        self.city_input.setText(self.prefs.get("city", ""))

        self.st_label = QLabel("St:")
        self.st_input = QLineEdit()
        self.st_input.setText(self.prefs.get("st", ""))

        self.zip_label = QLabel("Zip:")
        self.zip_input = QLineEdit()
        self.zip_input.setText(self.prefs.get("zip", ""))

        city_st_zip_layout = QHBoxLayout()
        city_st_zip_layout.addWidget(self.city_input)
        city_st_zip_layout.addWidget(self.st_input)
        city_st_zip_layout.addWidget(self.zip_input)

# PROVIDER
        self.provider_label = QLabel("Provider Name:")
        self.provider_input = QLineEdit()
        self.provider_input.setText(self.prefs.get("provider_name", ""))

# PHONE
        self.phone_label = QLabel("Phone Number:")
        self.phone_input = QLineEdit()
        self.phone_input.setText(self.prefs.get("phone_number", ""))

        # Add RegExp validator to the phone input field
        reg_ex = QRegExp("^\d{3}-\d{3}-\d{4}$")
        input_validator = QRegExpValidator(reg_ex, self.phone_input)
        self.phone_input.setValidator(input_validator)

# layout for preference options
        layout = QFormLayout()
        layout.addRow(self.theme_label, theme_layout)
        # layout.addRow(self.theme_label, self.theme_dropdown)
        layout.addRow(self.business_label, self.business_input)
        layout.addRow(self.image_button)
        layout.addRow(self.image_label, self.image_field)
        layout.addRow(self.address_label, self.address_input)
        layout.addRow(QLabel("City, St, Zip:"), city_st_zip_layout)
        layout.addRow(self.provider_label, self.provider_input)
        layout.addRow(self.phone_label, self.phone_input)

# SAVE AND CANCEL BUTTONS
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_preferences)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)

        # Create main layout for the dialog
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)

        button_layout = QHBoxLayout()
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.exec()

    def select_image(self):
        image_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if image_path:
            self.image_field.setText(image_path)

    def load_settings(self):
        # Load existing preferences
        try:
            with open('settings.json', 'r') as f:
                self.prefs = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.prefs = {}  # Ignore if the file does not exist or is not a valid JSON

    def save_preferences(self):
        prefs = {}
        try:
            with open('settings.json', 'r') as f:
                prefs = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        for key, new_value in {
            "theme": self.theme_dropdown.currentText(),
            "business_info": self.business_input.text(),
            "business_logo": self.image_field.text(),
            "business_address": self.address_input.text(),
            "city": self.city_input.text(),
            "st": self.st_input.text(),
            "zip": self.zip_input.text(),
            "provider_name": self.provider_input.text(),
            "phone_number": self.phone_input.text()
        }.items():
            old_value = prefs.get(key)
            if new_value or not old_value:
                prefs[key] = new_value
            elif old_value:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Question)
                msg.setText(f"Do you want to overwrite the existing value '{old_value}' for '{key}'?")
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                if msg.exec_() == QMessageBox.Yes:
                    prefs[key] = new_value

        # Save preferences to a JSON file
        with open('settings.json', 'w') as f:
            json.dump(prefs, f)
        self.accept()

class SearchEditDeletePopup(QDialog):

    def __init__(self, parent=None):
        super(SearchEditDeletePopup, self).__init__(parent)
        self.setWindowTitle("Search, Edit, Delete Patient")

        # Validators
        alphanumeric = QRegExp("[a-zA-Z0-9]+")
        validator = QRegExpValidator(alphanumeric)


               # Create input fields
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.search_records)

        self.search_table = QTableWidget(0, 3)
        self.search_table.setHorizontalHeaderLabels(["First Name", "Last Name", "ID"])
        self.search_table.setFixedHeight(200)
        self.search_table.cellClicked.connect(self.populate_fields)

        self.first_name_input = QLineEdit()
        self.first_name_input.editingFinished.connect(self.generate_id)

        self.last_name_input = QLineEdit()
        self.last_name_input.editingFinished.connect(self.generate_id)

        self.date_of_birth_input = QDateEdit()
        self.date_of_birth_input.setCalendarPopup(True)
        self.date_of_birth_input.editingFinished.connect(self.generate_id)

        self.gender_input = QComboBox()
        self.gender_input.addItem("Male")
        self.gender_input.addItem("Female")

        self.id_input = QLineEdit()
        self.current_patient_id = None

        self.warning_input = QTextEdit()
        self.special_note_input = QTextEdit()

        # Create a layout for the input fields
        personal_details_layout = QFormLayout()
        personal_details_layout.addRow("First Name:", self.first_name_input)
        personal_details_layout.addRow("Last Name:", self.last_name_input)

        other_details_layout = QFormLayout()
        other_details_layout.addRow("Date of Birth:", self.date_of_birth_input)
        other_details_layout.addRow("Gender:", self.gender_input)
        other_details_layout.addRow("Warning:", self.warning_input)
        other_details_layout.addRow("Special Note:", self.special_note_input)
        other_details_layout.addRow("ID:", self.id_input)

        # Grouping
        personal_details_group = QGroupBox("Personal Details")
        personal_details_group.setLayout(personal_details_layout)

        other_details_group = QGroupBox("Other Details")
        other_details_group.setLayout(other_details_layout)

        # Create buttons for apply changes, save and cancel actions
        self.apply_button = QPushButton("Apply Changes")
        self.apply_button.clicked.connect(self.apply_changes)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save)

        self.delete_button = QPushButton("Delete Record")
        self.delete_button.clicked.connect(self.delete_record)
        self.delete_button.setEnabled(False)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)

        # Create a main layout for the dialog
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel("Search:"))
        main_layout.addWidget(self.search_input)
        main_layout.addWidget(self.search_table)
        main_layout.addWidget(personal_details_group)
        main_layout.addWidget(other_details_group)

        # Put the Apply Changes, Delete Record, and Cancel buttons in one row
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.apply_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(cancel_button)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.resize(800, self.height())  # set the width to 800px
        self.exec()

    def search_records(self):
        self.search_table.setRowCount(0)
        query = self.search_input.text().lower()

        # Load existing patient data from the JSON file, if any
        existing_data = []
        try:
            with open("patients_names.json", "r") as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            pass

        # Find and display matches
        for patient in existing_data:
            first_name = patient.get('first_name', '').lower()
            last_name = patient.get('last_name', '').lower()
            patient_id = patient.get('patient_id', '')
            if patient_id is not None:
                patient_id = patient_id.lower()

            if query in first_name or query in last_name or query in patient_id:
                row_position = self.search_table.rowCount()
                self.search_table.insertRow(row_position)
                self.search_table.setItem(row_position, 0, QTableWidgetItem(patient['first_name']))
                self.search_table.setItem(row_position, 1, QTableWidgetItem(patient['last_name']))
                self.search_table.setItem(row_position, 2, QTableWidgetItem(patient['patient_id']))
                self.search_table.setCellWidget(row_position, 3, QLabel())
                self.search_table.cellWidget(row_position, 3).setProperty('patient', patient)

    def populate_fields(self, item):
        # Retrieve the patient data from the item
        patient = self.search_table.cellWidget(row, 3).property('patient')
        # Update the current patient id
        self.current_patient_id = patient["patient_id"]

        # Assuming `patient` is a dict object with patient details.
        self.first_name_input.setText(patient["first_name"])
        self.last_name_input.setText(patient["last_name"])
        self.date_of_birth_input.setDate(QDate.fromString(patient["date_of_birth"], "MMddyyyy"))
        index = self.gender_input.findText(patient["gender"])
        self.gender_input.setCurrentIndex(index)
        self.id_input.setText(patient["patient_id"])
        self.warning_input.setText(patient["warning"])
        self.special_note_input.setText(patient["special_note"])

        self.delete_button.setEnabled(True)

    def delete_record(self):
        if self.current_patient_id is None:
            QMessageBox.warning(self, 'Warning', 'No patient selected.')
            return

        existing_data = []
        try:
            with open("patients_names.json", "r") as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            pass

        # Check if patient with the same ID exists
        existing_data = [pat for pat in existing_data if pat.get('patient_id') != self.current_patient_id]

        # Save the updated data to the JSON file
        with open("patients_names.json", "w") as file:
            json.dump(existing_data, file, indent=2)

        # Clear fields and search results
        self.clear_fields()
        self.search_records()  # This will now clear the search input field


    def apply_changes(self):
        # Get the values from the input fields
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        date_of_birth = self.date_of_birth_input.date().toString("MMddyyyy")
        gender = self.gender_input.currentText()
        warning = self.warning_input.toPlainText()
        special_note = self.special_note_input.toPlainText()

        # Generate patient id
        patient_id = self.id_input.text()

        # Create a dictionary object with the patient details
        patient = {
            "first_name": first_name,
            "last_name": last_name,
            "date_of_birth": date_of_birth,
            "gender": gender,
            "warning": warning,
            "special_note": special_note,
            "patient_id": patient_id
        }

        # Load existing patient data from the JSON file, if any
        existing_data = []
        try:
            with open("patients_names.json", "r") as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            pass

        # Check if patient with the same ID already exists
        for index, existing_patient in enumerate(existing_data):
            if existing_patient.get('patient_id') == self.current_patient_id:
                existing_data[index] = patient
                break
        else:
            # If no existing patient was found, add the new patient to the existing data
            existing_data.append(patient)

        # Save the updated data to the JSON file
        with open("patients_names.json", "w") as file:
            json.dump(existing_data, file, indent=2)

        # Clear the input fields and the current patient id
        self.clear_fields()
        self.current_patient_id = None
        self.search_input.clear()

    def clear_fields(self):
        self.first_name_input.clear()
        self.last_name_input.clear()
        self.date_of_birth_input.clear()
        self.gender_input.setCurrentIndex(0)
        self.id_input.clear()
        self.warning_input.clear()
        self.special_note_input.clear()
        self.search_input.clear()
        self.current_patient_id = None  # Clear current patient id
        self.delete_button.setEnabled(False)  # Disable the delete button


    def generate_id(self):

        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        date_of_birth = self.date_of_birth_input.date().toString("MMddyyyy")

        first_initial = first_name[0].upper() if first_name else ''
        last_initial = last_name[0].upper() if last_name else ''

        patient_id = date_of_birth + last_initial + first_initial
        self.id_input.setText(patient_id)

    def data_was_saved_successfully(self, patient_id):
        # Check if the patient record was saved by checking if it exists in the saved data
        try:
            with open("patients_names.json", "r") as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            return False

        if any(pat.get('patient_id') == patient_id for pat in existing_data):
            return True

        return False

    def save(self):
        # Get the values from the input fields
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        date_of_birth = self.date_of_birth_input.date().toString("MMddyyyy")
        gender = self.gender_input.currentText()
        warning = self.warning_input.toPlainText()
        special_note = self.special_note_input.toPlainText()

        # Generate patient id
        patient_id = self.id_input.text()

        # Create a dictionary object with the patient details
        patient = {
            "first_name": first_name,
            "last_name": last_name,
            "date_of_birth": date_of_birth,
            "gender": gender,
            "warning": warning,
            "special_note": special_note,
            "patient_id": patient_id
        }

        # Load existing patient data from the JSON file, if any
        existing_data = []
        try:
            with open("patients_names.json", "r") as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            pass

        if not self.current_patient_id:  # Only add a new patient if there is no current patient id
            # Check if patient with the same ID already exists
            if any(pat.get('patient_id') == patient_id for pat in existing_data):
                # Generate a unique identifier and append it to the ID
                unique_id = len(existing_data) + 1
                patient_id += str(unique_id)
                self.id_input.setText(patient_id)
                patient["patient_id"] = patient_id
                QMessageBox.warning(self, 'Warning', 'A patient with the initial ID already exists. A unique identifier has been appended to the ID.')

            # Add the new patient to the existing data
            existing_data.append(patient)

        else:
            # If there is a current patient id, just apply changes to the existing record
            for index, existing_patient in enumerate(existing_data):
                if existing_patient.get('patient_id') == self.current_patient_id:
                    existing_data[index] = patient
                    break

        # Save the updated data to the JSON file
        with open("patients_names.json", "w") as file:
            json.dump(existing_data, file, indent=2)

        # Clear the input fields and the current patient id
        self.clear_fields()
        self.current_patient_id = None
        self.search_input.clear()


class MenuBar(QMenuBar):

    def __init__(self, parent=None):
        super(MenuBar, self).__init__(parent)
        self.file_menu = self.addMenu("File")
        self.edit_menu = self.addMenu("Edit")

        self.create_actions()
        self.create_file_menu()
        self.create_edit_menu()
    def create_actions(self):
        self.create_new_patient_action = QAction("Create New Patient", self)
        self.create_new_patient_action.triggered.connect(self.open_create_patient_popup)
        self.look_at_patient_record_action = QAction("Look at Patient Record", self)
        self.look_at_patient_record_action.triggered.connect(self.open_look_at_patient_record_popup)
        self.preferences_action = QAction("Settings", self)
        self.preferences_action.triggered.connect(self.open_settings_popup)
    def create_file_menu(self):
        self.file_menu.addAction(self.create_new_patient_action)
        self.file_menu.addAction(self.look_at_patient_record_action)
        self.file_menu.addAction(self.preferences_action)
    def create_edit_menu(self):
        pass  # Add your actions and submenus for the Edit menu here
    def open_create_patient_popup(self):
        popup = CreatePatientPopup(self)

    def open_settings_popup(self):
        popup = SettingsPopup(self)

    def open_look_at_patient_record_popup(self):
        popup = LookAtPatientRecord(self)

class ToolBar(QToolBar):
    def __init__(self, parent=None):
        super(ToolBar, self).__init__(parent)
        self.setIconSize(QSize(32, 32))

        self.create_actions()
        self.add_actions()

    def create_actions(self):
        self.create_new_patient_action = QAction(qta.icon('mdi.folder-plus', color='#f1d592'), "Create New Patient", self)
        self.create_new_patient_action.setStatusTip("Create New Patient")
        self.create_new_patient_action.setToolTip("Create New Patient")
        self.create_new_patient_action.triggered.connect(self.open_create_patient_popup)

        self.look_at_patient_record_action = QAction(qta.icon('mdi.folder-open', color='#f1d592'), "Look At Patient Record", self)
        self.look_at_patient_record_action.setStatusTip("Look At Patient Record")
        self.look_at_patient_record_action.triggered.connect(self.open_look_at_patient_record_popup)

    def add_actions(self):
        self.addAction(self.create_new_patient_action)
        self.addAction(self.look_at_patient_record_action)

    def open_create_patient_popup(self):
        popup = CreatePatientPopup(self)

    def open_look_at_patient_record_popup(self):
        popup = LookAtPatientRecord(self)

class BackgroundImageLabel(QLabel):
    def __init__(self):
        super(BackgroundImageLabel, self).__init__()
        self.setAlignment(Qt.AlignCenter)
        self.load_image_path()
        self.set_layout()

    def load_image_path(self):
        try:
            with open('settings.json', 'r') as f:
                prefs = json.load(f)
                image_path = prefs.get("business_logo", "")
                self.image_path = image_path if os.path.isfile(image_path) else ""
        except (FileNotFoundError, json.JSONDecodeError):
            self.image_path = ""

    def set_layout(self):
        if self.image_path:
            pixmap = QPixmap(self.image_path)
            self.setPixmap(pixmap)
            self.setStyleSheet("QLabel { background-repeat: no-repeat; }")
        else:
            self.setText("No image found")

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Load preferences
        self.load_settings()
        # setup stylesheet

        # Create and show your main window
        self.setWindowTitle("Chiropractic SOAP Note Program")
        screen_width = QApplication.desktop().screenGeometry().width()
        screen_height = QApplication.desktop().screenGeometry().height()
        self.setGeometry(-1920, 25, screen_width, screen_height-75)

        # Create a main widget and a vertical layout
        main_widget = QWidget(self)
        layout = QVBoxLayout(main_widget)
        # Create and add the BackgroundImageLabel to the layout
        background_label = BackgroundImageLabel()
        layout.addWidget(background_label)

                # Set the main widget as the central widget
        self.setCentralWidget(main_widget)

# MENU BAR
        self.create_toolbar()
        self.create_menu_bar()

    def load_settings(self):
        try:
            if os.path.exists('settings.json'):
                with open('settings.json', 'r') as f:
                    prefs = json.load(f)

                theme = prefs.get('theme')
                background_image_path = prefs.get('background_image_path')

                if theme:
                    apply_stylesheet(self, theme=theme)

        except Exception as e:
            print(f"Failed to load preferences: {e}")

    # Load other preferences here as needed
    def create_menu_bar(self):
        menu_bar = MenuBar(self)
        self.setMenuBar(menu_bar)
    def create_toolbar(self):
        toolbar = ToolBar(self)
        self.addToolBar(toolbar)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
