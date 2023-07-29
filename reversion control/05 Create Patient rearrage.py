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

        # Create input fields
        self.first_name_input = QLineEdit()
        self.last_name_input = QLineEdit()
        self.date_of_birth_input = QDateEdit()
        self.date_of_birth_input.setCalendarPopup(True)
        self.gender_input = QComboBox()
        self.gender_input.addItem("Male")
        self.gender_input.addItem("Female")
        self.id_input = QLineEdit()
        self.id_input.setMaxLength(10)  # Set maximum length to 10 characters
        self.address_input = QLineEdit()
        self.warning_input = QLineEdit()
        self.special_note_input = QLineEdit()

        # Create a layout for the input fields
        layout = QGridLayout()
        layout.addWidget(QLabel("First Name:"), 0, 0)
        layout.addWidget(self.first_name_input, 0, 1)
        layout.addWidget(QLabel("Last Name:"), 1, 0)
        layout.addWidget(self.last_name_input, 1, 1)
        layout.addWidget(QLabel("Date of Birth:"), 2, 0)
        layout.addWidget(self.date_of_birth_input, 2, 1)
        layout.addWidget(QLabel("Gender:"), 3, 0)
        layout.addWidget(self.gender_input, 3, 1)
        layout.addWidget(QLabel("ID:"), 4, 0)
        layout.addWidget(self.id_input, 4, 1)
        layout.addWidget(QLabel("Address:"), 5, 0)
        layout.addWidget(self.address_input, 5, 1)
        layout.addWidget(QLabel("Warning:"), 6, 0)
        layout.addWidget(self.warning_input, 6, 1)
        layout.addWidget(QLabel("Special Note:"), 7, 0)
        layout.addWidget(self.special_note_input, 7, 1)

        # Create buttons for save and cancel actions
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout = QHBoxLayout()
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        # Create left and right layouts for the dialog
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        left_layout.addLayout(button_layout)
        left_layout.addStretch()

        right_layout.addLayout(layout)

        # Create a group box for left layout
        left_group_box = QGroupBox()
        left_group_box.setLayout(left_layout)

        # Create a main layout for the dialog
        main_layout = QHBoxLayout()
        main_layout.addWidget(left_group_box)
        main_layout.addLayout(right_layout)
        main_layout.setStretch(0, 1)  # make left layout smaller
        main_layout.setStretch(1, 3)  # make right layout three times larger

        self.setLayout(main_layout)
        self.resize(800, self.height())  # set the width to 800px
        self.exec()


    def save(self):
        # Get the values from the input fields
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        date_of_birth = self.date_of_birth_input.date().toString("MM-dd-yyyy")
        gender = self.gender_input.currentText()
        patient_id = self.id_input.text()
        address = self.address_input.text()
        warning = self.warning_input.text()
        special_note = self.special_note_input.text()

        # Create a dictionary object with the patient details
        patient = {
            "first_name": first_name,
            "last_name": last_name,
            "date_of_birth": date_of_birth,
            "gender": gender,
            "id": patient_id,
            "address": address,
            "warning": warning,
            "special_note": special_note
        }

        # Load existing patient data from the JSON file, if any
        existing_data = []
        try:
            with open("patients_names.json", "r") as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            pass

        # Add the new patient to the existing data
        existing_data.append(patient)

        # Save the updated data to the JSON file
        with open("patients_names.json", "w") as file:
            json.dump(existing_data, file)

        # Close the dialog
        self.accept()



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
