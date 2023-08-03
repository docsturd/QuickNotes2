import sys
import json
import os
from datetime import *

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from qt_material import *
import qtawesome as qta # qta-browser

###  IMPORTANT FUNCTIONS LOAD AND WRITE  ###
def load_data():
    existing_data = []
    try:
        with open("patients_names.json", "r") as file:
            existing_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    return existing_data
def load_settings():
    settings_data = []
    try:
        with open("settings.json", "r") as file:
            settings_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    return settings_data
def write_data(data):
    with open("patients_names.json", "w") as file:
        json.dump(data, file, indent=2)

class PrintPreviewToolbar(QToolBar):
    def __init__(self, text_edit, parent=None):
        super(PrintPreviewToolbar, self).__init__(parent)
        self.text_edit = text_edit
        self.initToolbar()

    def initToolbar(self):
        # Create a printer
        self.printer = QPrinter(QPrinter.HighResolution)

        # Add print preview action

        print_preview_action = QAction(qta.icon('mdi.printer-eye', color='#f1d592'), "Print preview", self)
        print_preview_action.triggered.connect(self.printPreview)
        self.addAction(print_preview_action)

        # Add print action
        print_action = QAction(qta.icon('mdi.printer', color='#f1d592'), "Print", self)
        print_action.triggered.connect(self.print)
        self.addAction(print_action)

    def printPreview(self):
        # Open print preview dialog
        preview = QPrintPreviewDialog(self.printer, self)
        preview.paintRequested.connect(self.paintPreview)

        # Add Save and Save As options
        toolbar = preview.findChildren(QToolBar)[0]

        save_action = QAction("Save", toolbar)
        save_action.triggered.connect(self.savePreview)
        toolbar.addAction(save_action)

        save_as_action = QAction("Save As", toolbar)
        save_as_action.triggered.connect(self.saveAsPreview)
        toolbar.addAction(save_as_action)

        # Set the window size and allow full screen
        preview.setWindowState(Qt.WindowMaximized)
        preview.showMaximized()

    def savePreview(self):
        # Save the print preview as a file
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Print Preview", "", "PDF Files (*.pdf);;All Files (*)")

        if file_path:
            printer = self.printer
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(file_path)
            printer.setPageMargins(0, 0, 0, 0, QPrinter.Millimeter)
            printer.setFullPage(True)

            preview = QPrintPreviewDialog(printer, self)
            preview.paintRequested.connect(self.paintPreview)
            preview.exec_()

    def saveAsPreview(self):
        # Save the print preview as a new file
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Print Preview As", "", "PDF Files (*.pdf);;All Files (*)")

        if file_path:
            printer = self.printer
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(file_path)
            printer.setPageMargins(0, 0, 0, 0, QPrinter.Millimeter)
            printer.setFullPage(True)

            preview = QPrintPreviewDialog(printer, self)
            preview.paintRequested.connect(self.paintPreview)
            preview.exec_()

    def paintPreview(self, printer):
        # Render the QTextEdit content into the printer
        try:
            self.setStandardFontSize()
            self.text_edit.print_(printer)
        except Exception as e:
            # Handle any potential printing errors
            print(f"Error occurred during print preview: {e}")

    def print(self):
        # Open print dialog
        try:
            self.setStandardFontSize()
            dialog = QPrintDialog(self.printer, self)
            if dialog.exec_() == QPrintDialog.Accepted:
                self.text_edit.print_(self.printer)
        except Exception as e:
            # Handle any potential printing errors
            print(f"Error occurred during printing: {e}")

    def setStandardFontSize(self):
        # Set the font size of the QTextEdit to a standard value
        font = self.text_edit.currentFont()
        font.setPointSize(10)  # Adjust the font size as desired
        cursor = self.text_edit.textCursor()
        format = QTextCharFormat()
        format.setFont(font)
        cursor.select(QTextCursor.Document)
        cursor.setCharFormat(format)
        self.text_edit.setTextCursor(cursor)
    def generateFileName(self):
        # Generate a unique filename for the PDF using patient ID and current date
        patient_id = "12345"  # Replace with the actual patient ID
        current_date = datetime.now().strftime("%m%d%Y")
        file_name = f"SOAP_{patient_id}_{current_date}.pdf"
        return file_name
class CreatePatientPopup(QDialog):

    def __init__(self, parent=None):
        super(CreatePatientPopup, self).__init__(parent)
        screen = QDesktopWidget().screenGeometry()
        width = int(screen.width() * .95)  # 100% of screen width
        height = int(screen.height() * 0.75)  # 50% of screen height
        self.resize(width, height)
        screen_pos = screen.topLeft() # Get the position of the screen's top-left corner
        self.move(screen_pos.x() + 20, screen_pos.y() + 110) # Move the window 100px down from the top of the screen
        self.setWindowTitle("Create, Edit, Delete Patient")

    # Create input fields
        self.first_name_input = QLineEdit()
        self.first_name_input.editingFinished.connect(self.generate_id)

        self.last_name_input = QLineEdit()
        self.last_name_input.editingFinished.connect(self.generate_id)

        self.date_of_birth_input = QLineEdit()
        self.date_of_birth_input.setPlaceholderText("MMDDYYYY")  # placeholder text
        regex = QRegExp("(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])(19|20)\d{2}")
        self.date_of_birth_input.setValidator(QRegExpValidator(regex))  # allowing only valid dates
        # connect generate_id() to textChanged signal
        self.date_of_birth_input.textChanged.connect(self.generate_id)
        self.date_of_birth_input.editingFinished.connect(self.handle_date_input)

        self.gender_input = QComboBox()
        self.gender_input.addItem("Male")
        self.gender_input.addItem("Female")

        self.id_input = QLineEdit()
        self.current_patient_id = None

        self.warning_input = QTextEdit()
        self.warning_input.setFixedHeight(75)
        self.special_note_input = QTextEdit()
        self.special_note_input.setFixedHeight(50)

    # Create buttons for apply changes, save and cancel actions
        self.sort_by_last_name_radio = QRadioButton("Sort by Last Name")
        self.sort_by_last_name_radio.setChecked(True)  # Set as default
        self.sort_by_last_name_radio.toggled.connect(self.sort_list)

        self.sort_by_patient_id_radio = QRadioButton("Sort by Patient ID")
        self.sort_by_patient_id_radio.toggled.connect(self.sort_list)

        font = QFont()
        font.setPointSize(100)  # Change the number to adjust the size
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.search_records)
        self.search_list = QListWidget()
        self.search_list.setFixedHeight(100)
        self.search_list.itemClicked.connect(self.populate_fields)

        self.add_new_record_button = QPushButton("Add New Record")  # New button
        self.add_new_record_button.clicked.connect(self.add_new_record)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save)

        # self.edit_button = QPushButton("Edit")
        # self.edit_button.clicked.connect(self.edit_record)

        self.delete_button = QPushButton("Delete Record")
        self.delete_button.clicked.connect(self.delete_record)
        self.delete_button.setEnabled(False)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)

    # Create a layout for the input fields
        personal_details_layout = QFormLayout()
        personal_details_layout.addRow("First Name:", self.first_name_input)
        personal_details_layout.addRow("Last Name:", self.last_name_input)

        other_details_layout = QFormLayout()
        other_details_layout.addRow("Birthday:", self.date_of_birth_input)
        other_details_layout.addRow("Gender:", self.gender_input)
        other_details_layout.addRow("Warning:", self.warning_input)
        other_details_layout.addRow("Special Note:", self.special_note_input)
        other_details_layout.addRow("ID:", self.id_input)

        # Create patient Notes
        # Define the exam_types
        exam_types = ['New Patient Exam', 'Est Patient Exam', 'Soap Note', 'XRay Report', 'Forms']

        # Create the button grid layout
        patient_notes_button_layout = QGridLayout()

        # Add buttons with names from the exam_types list
        for i, patient_notes_name in enumerate(exam_types):
            row = i // 2
            column = i % 2
            button = QPushButton(patient_notes_name)
            button.setFixedSize(175, 100)  # Set the button size
            button.clicked.connect(getattr(self, f"handle_{patient_notes_name.replace(' ', '_').lower()}"))
            patient_notes_button_layout.addWidget(button, row, column)

    # Create a widget to hold the grid layout
        patient_notes_button_widget = QWidget()
        patient_notes_button_widget.setLayout(patient_notes_button_layout)

    # Grouping Data Feilds
        personal_details_group = QGroupBox("Personal Details")
        personal_details_group.setLayout(personal_details_layout)
        other_details_group = QGroupBox("Other Details")
        other_details_group.setLayout(other_details_layout)

    # Grouping Radio buttons
        sort_radio_group = QGroupBox("Sort by:")
        sort_radio_layout = QVBoxLayout()
        # Add padding: left, top, right, bottom
        sort_radio_layout.setContentsMargins(5, 5, 5, 5)
        sort_radio_layout.addWidget(self.sort_by_last_name_radio)
        sort_radio_layout.addWidget(self.sort_by_patient_id_radio)
        sort_radio_group.setLayout(sort_radio_layout)
    # Grouping Search Widgets
        search_group = QGroupBox("Search")

        search_layout = QVBoxLayout()
        # Add padding: left, top, right, bottom
        search_layout.setContentsMargins(5, 5, 5, 5)
        # search_layout.addWidget(QLabel("Search:"))
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_list)
        search_group.setLayout(search_layout)

    # Create a layout for the left column
        left_column_layout = QVBoxLayout()
        # Add padding: left, top, right, bottom
        left_column_layout.setContentsMargins(5, 5, 5, 5)
        left_column_layout.addWidget(sort_radio_group)
        left_column_layout.addWidget(search_group)
        left_column_layout.addWidget(self.add_new_record_button)  # Add the new button
        left_column_layout.addWidget(save_button)
        # left_column_layout.addWidget(self.edit_button)
        left_column_layout.addWidget(self.delete_button)
        left_column_layout.addWidget(cancel_button)
        left_column_layout.addStretch(1)  # Add a stretch at the end
        left_column_widget = QWidget()
        left_column_widget.setLayout(left_column_layout)

    # Create a line widget for vertical separation
        line_widget = QFrame()
        line_widget.setFrameShape(QFrame.VLine)
        line_widget.setStyleSheet("color: #ffffff")  # Set line color (black)

    # Create a layout for the right column
        right_column_layout = QVBoxLayout()
        # Add padding: left, top, right, bottom
        right_column_layout.setContentsMargins(5, 5, 5, 5)
        right_column_layout.addWidget(personal_details_group)
        right_column_layout.addWidget(other_details_group)
        right_column_widget = QWidget()
        right_column_widget.setLayout(right_column_layout)


    # Create a main layout for the dialog
        main_layout = QHBoxLayout()
        main_layout.addWidget(left_column_widget)
        main_layout.addWidget(line_widget)
        main_layout.addWidget(right_column_widget)
        main_layout.addWidget(line_widget)
        main_layout.addWidget(patient_notes_button_widget)

    # Modify the stretch factors to set the width of the columns
        main_layout.setStretchFactor(left_column_widget, 1)
        main_layout.setStretchFactor(right_column_widget, 3)
        main_layout.setStretchFactor(patient_notes_button_widget, 1)

        self.setLayout(main_layout)
        self.resize(1000, self.height())  # set the width to 800px
        self.data = load_data()
        self.sort_list()  # Sort the data initially
        self.search_records()  # Populate and display the sorted data in the QListWidget
        self.exec()

    def search_records(self):
        self.search_list.clear()
        query = self.search_input.text().lower()
        existing_data = self.data

        # Find and display matches
        for patient in existing_data:
            first_name = patient.get('first_name', '').lower()
            last_name = patient.get('last_name', '').lower()
            patient_id = patient.get('patient_id', '')

            if patient_id is not None:
                patient_id = patient_id.lower()

            if query in first_name or query in last_name or query in patient_id:
                if self.sort_by_last_name_radio.isChecked():
                    # Display last name, first name
                    item = QListWidgetItem(patient['last_name'] + ', ' + patient['first_name'])
                else:
                    # Display patient ID
                    item = QListWidgetItem(patient['patient_id'])
                item.setData(Qt.UserRole, patient)
                self.search_list.addItem(item)
    def sort_list(self):
        if self.sort_by_last_name_radio.isChecked():
            # If 'Sort by Last Name' radio button is checked
            self.data.sort(key=lambda x: x['last_name'].lower())
        elif self.sort_by_patient_id_radio.isChecked():
            # If 'Sort by Patient ID' radio button is checked
            self.data.sort(key=lambda x: x['patient_id'].lower())

        self.search_records()  # Refresh the search records
        # Populate the search list widget with sorted data
        self.search_list.clear()
        for patient in self.data:
            if self.sort_by_last_name_radio.isChecked():
                item = QListWidgetItem(patient['last_name'] + ', ' + patient['first_name'])
            else:
                item = QListWidgetItem(patient['patient_id'])
            item.setData(Qt.UserRole, patient)
            self.search_list.addItem(item)
    def populate_fields(self, item):
        # Retrieve the patient data from the item
        patient = item.data(Qt.UserRole)
        # Update the current patient id
        self.current_patient_id = patient["patient_id"]

        # Assuming `patient` is a dict object with patient details.
        self.first_name_input.setText(patient["first_name"])
        self.last_name_input.setText(patient["last_name"])
        # self.date_of_birth_input.setDate(QDate.fromString(patient["date_of_birth"], "MMddyyyy"))
        # Format the date string to the desired format before setting the text
        date_of_birth = QDate.fromString(patient["date_of_birth"], "MMddyyyy")
        age = QDate.currentDate().year() - date_of_birth.year() - ((QDate.currentDate().month(), QDate.currentDate().day()) < (date_of_birth.month(), date_of_birth.day()))
        self.date_of_birth_input.setText(f"Age: {age}, DOB: {date_of_birth.toString('MM/dd/yyyy')}")

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

        # Check if patient with the same ID exists
        self.data = [pat for pat in self.data if pat.get('patient_id') != self.current_patient_id]

        write_data(self.data) # Save the updated data to the JSON file
        self.clear_fields() # Clear fields and search results
        self.search_records()  # Refresh the QListWidget
        self.current_patient_id = None
        self.search_input.clear()

    def handle_date_input(self):
        text = self.date_of_birth_input.text()
        if len(text) == 8:  # If a complete date is entered
            date = QDate.fromString(text, "MMddyyyy")
            today = QDate.currentDate()
            age = today.year() - date.year() - ((today.month(), today.day()) < (date.month(), date.day()))
            formatted_date = date.toString("MM/dd/yyyy")
            self.date_of_birth_input.setText(f"Age: {age}, DOB: {formatted_date}")
    def generate_id(self):
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        dob_text = self.date_of_birth_input.text().split(",")[1].strip() if ',' in self.date_of_birth_input.text() else ''
        # check that dob_text can be split into at least two parts
        if ": " in dob_text:
            date_of_birth = QDate.fromString(dob_text.split(": ")[1], "MM/dd/yyyy").toString("MMddyyyy") if dob_text else ''
        else:
            date_of_birth = ''

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
    def refresh_list(self):
        self.search_list.clear()
        self.search_records()
    def save(self):
        # Get the values from the input fields
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()

        # Check if required fields are empty
        if not first_name or not last_name:
            QMessageBox.warning(self, 'Warning', 'First name and last name are required.')
            return

        # Continue with saving the record
        # date_of_birth = self.date_of_birth_input.date().toString("MMddyyyy")
        dob_text = self.date_of_birth_input.text().split(",")[1].strip() if ',' in self.date_of_birth_input.text() else ''
        date_of_birth = QDate.fromString(dob_text.split(": ")[1], "MM/dd/yyyy").toString("MMddyyyy") if dob_text else ''
        gender = self.gender_input.currentText()
        warning = self.warning_input.toPlainText()
        special_note = self.special_note_input.toPlainText()
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

        existing_data = self.data  # Load existing patient data from the JSON file, if any

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

        write_data(self.data)  # Save the updated data to the JSON file
        self.clear_fields()  # Clear the input fields and the current patient id
        self.current_patient_id = None
        self.search_input.clear()
        self.refresh_list()
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
    def add_new_record(self):
        self.save() # Save the current record
        self.clear_fields() # Clear all fields

        # Disable the delete button as it is a new record
        self.delete_button.setEnabled(False)
    def handle_new_patient_exam(self):
        # Add your code here
        pass
    def handle_est_patient_exam(self):
        # Add your code here
        pass
    def handle_soap_note(self):
        # Retrieve the patient data from the current selected item
        if self.search_list.currentItem():
            patient = self.search_list.currentItem().data(Qt.UserRole)
        else:
            patient = None

        # Get the main window (parent of the CreatePatientPopup)
        main_window = self.parentWidget()

        self.soap_note_popup = Soap_Note(main_window, patient)
        self.soap_note_popup.show()
        # Close the CreatePatientPopup
        self.close()
    def handle_xray_report(self):
        # Add your code here
        pass
    def handle_forms(self):
        # Add your code here
        pass

#####  Popup for exam
class NewPatientExamPopup(QDialog):
    pass
class EstPatientExamPopup(QDialog):
    pass
class Soap_Note(QDialog):

    def __init__(self, parent=None, patient=None):
        super(Soap_Note, self).__init__(parent)
# Get screen size
        screen = QDesktopWidget().screenGeometry()
        width = int(screen.width() * .95)  # 100% of screen width
        height = int(screen.height() * 0.75)  # 50% of screen height
        self.resize(width, height)
        screen_pos = screen.topLeft() # Get the position of the screen's top-left corner
        self.move(screen_pos.x() + 20, screen_pos.y() + 110) # Move the window 100px down from the top of the screen
        self.setWindowTitle("SOAP NOTE")

# Load Practic data
        self.settings = load_settings()
# Patient data
        self.patient = patient

# Check if the patient record has a warning
        if patient and 'warning' in patient and patient['warning']:
            self.show_warning(patient['warning'])
        else:
            self.warning_text = None

# Create the tab widget with 4 tabs
        self.tab_widget = QTabWidget()
        self.tab_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.create_tabs()

######################### ADD TEXT TO QTextEdit #####################
### create a QTextEdit field, appending information to it, and
### controlling the alignment of the appended text.

# Create text edit field
        self.text_edit = QTextEdit()
        self.text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # creates an instance of PrintPreviewToolbar
        self.print_preview_toolbar = PrintPreviewToolbar(self.text_edit, self)
    ## Append patient and business information to the text edit field
        business_info = self.get_business_info()

    ## Create a new block with center alignment for business info
        cursor = self.text_edit.textCursor()
        format = QTextBlockFormat()
        format.setAlignment(Qt.AlignCenter)
        cursor.insertBlock(format)
        cursor.insertText(business_info)

    # Switch back to left alignment for subsequent text
        format = QTextBlockFormat()
        format.setAlignment(Qt.AlignLeft)
        cursor.insertBlock(format)
        self.text_edit.setTextCursor(cursor)
    ## Append patient information to the text edit field
        self.text_edit.append(self.get_patient_info())


######################### end ADD TEXT TO QTextEdit #####################

# Create a splitter and add the tab widget and text edit field to it
        self.splitter = QSplitter(Qt.Horizontal)  # PyQt5
        self.splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.splitter = QSplitter(Qt.Orientation.Horizontal)  # PyQt6, use this line instead if you are using PyQt6
        self.splitter.addWidget(self.tab_widget)
        self.splitter.addWidget(self.text_edit)

# Create a layout and add the splitter to it
        layout = QVBoxLayout()

# Add padding: left, top, right, bottom
        layout.setContentsMargins(5, 5, 5, 5)
        layout.addWidget(self.print_preview_toolbar)
        # layout.addWidget(self.info_label)
        layout.addWidget(self.splitter, 1)
        self.setLayout(layout)

# Calculate the widths for the tab widget and text edit field
        total_width = width - 40  # Adjust for the layout's left and right margins
        tab_widget_width = int(total_width * 0.75)
        text_edit_width = int(total_width * 0.25)
        self.splitter.setSizes([tab_widget_width, text_edit_width])

    def show_warning(self, warning):
        patient_name = f"{self.patient['first_name']} {self.patient['last_name']}"
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Patient Warning")
        msg.setInformativeText(f"<b>Warning for {patient_name}</b>:<br>{warning.upper()}")
        msg.setWindowTitle("Patient Warning")

    # Set the font size and text transformation for the informative text
        msg.setStyleSheet("QLabel{font-size: 20px;} QMessageBox QLabel { text-transform: uppercase; }")

        msg.exec_()
    def create_tabs(self):
        # Create 4 tabs
        for i in range(1, 5):
            tab = QWidget()
            tab_layout = QVBoxLayout()
            # Add padding: left, top, right, bottom
            tab_layout.setContentsMargins(5, 5, 5, 5)
            tab.setLayout(tab_layout)

            # Add a label to the tab
            label = QLabel(f"Content for tab {i}")
            tab_layout.addWidget(label)

            # Add the tab to the tab widget
            self.tab_widget.addTab(tab, f"Tab {i}")
    def get_patient_info(self):
        # Get patient information
        if self.patient:
            info = f"NAME:\t{self.patient['first_name']} {self.patient['last_name']}\nSEX:\t{self.patient['gender']}\nID:\t{self.patient['patient_id']}"
            # Add the warning if it exists
            if 'warning' in self.patient and self.patient['warning'] is not None:
                info += f"\n\nWARNING:\n{self.patient['warning']}"
        else:
            info = "No patient selected."

        return info
    def get_business_info(self):
        # Get patient information
        if self.settings:
            info = f"{self.settings['business_info']}\n{self.settings['business_address']} {self.settings['city']}, {self.settings['st']} {self.settings['zip']}  *  {self.settings['phone_number']}\n\n"
        else:
            info = "No Business information Available. goto File > Settings and add your information"
        return info
class XRayReportPopup(QDialog):
    pass
class FormsPopup(QDialog):
    pass

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
        # Add padding: left, top, right, bottom
        main_layout.setContentsMargins(5, 5, 5, 5)
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
            json.dump(prefs, f, indent=2)
        self.accept()

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
        self.preferences_action = QAction("Settings", self)
        self.preferences_action.triggered.connect(self.open_settings_popup)
    def create_file_menu(self):
        self.file_menu.addAction(self.create_new_patient_action)
        self.file_menu.addAction(self.preferences_action)
    def create_edit_menu(self):
        pass  # Add your actions and submenus for the Edit menu here
    def open_create_patient_popup(self):
        popup = CreatePatientPopup(self)

    def open_settings_popup(self):
        popup = SettingsPopup(self)

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

        # Add "XXX" action
        self.xxx_action = QAction(qta.icon('mdi.folder', color='#f1d592'), "XXX", self)
        self.xxx_action.setStatusTip("XXX StatusTip")
        self.xxx_action.setToolTip("XXX ToolTip")
        self.xxx_action.triggered.connect(self.open_xxx_popup)

    def add_actions(self):
        self.addAction(self.create_new_patient_action)
        self.addAction(self.xxx_action)  # Add the "XXX" action to the toolbar

    def open_create_patient_popup(self):
        popup = CreatePatientPopup(self)

    def open_xxx_popup(self):
        # Add the functionality for the "XXX" action here
        pass

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

        # Create and show your main window
        self.setWindowTitle("Chiropractic SOAP Note Program")
        screen_width = QApplication.desktop().screenGeometry().width()
        screen_height = QApplication.desktop().screenGeometry().height()
        # self.setGeometry(-1920, 25, screen_width, screen_height-75)
        self.setGeometry(0, 25, screen_width, screen_height-75)

        # Load preferences
        self.load_settings()

        # Create a main widget and a vertical layout
        main_widget = QWidget(self)
        layout = QVBoxLayout(main_widget)
        # Add padding: left, top, right, bottom
        layout.setContentsMargins(5, 5, 5, 5)
        # Create and add the BackgroundImageLabel to the layout
        background_label = BackgroundImageLabel()
        background_label.setAlignment(Qt.AlignCenter)  # Align label to the center
        layout.addWidget(background_label)

        # Create a QTextEdit for the document
        self.document_text_edit = QTextEdit(self)

        # Create a QLabel for the business information
        business_info_label = QLabel(self)
        business_info_text = (f"{self.settings['business_info']} {self.settings['business_address']} {self.settings['city']}, {self.settings['st']} {self.settings['zip']}\n\n{self.settings['provider_name']}")
        business_info_label.setText(business_info_text)
        business_info_label.setAlignment(Qt.AlignCenter)
        business_info_label.setWordWrap(True)  # Enable word wrapping for long lines

        layout.addWidget(business_info_label)


        # Set the main widget as the central widget
        self.setCentralWidget(main_widget)

# MENU BAR
        self.create_toolbar()
        self.create_menu_bar()


    def load_settings(self):
        try:
            if os.path.exists('settings.json'):
                with open('settings.json', 'r') as f:
                    self.settings = json.load(f)

                theme = self.settings.get('theme')
                background_image_path = self.settings.get('background_image_path')

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
