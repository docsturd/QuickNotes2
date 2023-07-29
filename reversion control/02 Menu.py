import sys
import json
import sqlite3
# from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QFormLayout, QLabel, QLineEdit, QPushButton
#
from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
from PyQt5.QtCore import *
from qt_material import apply_stylesheet
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
        self.setWindowTitle("Create New Patient")

        # First name input field
        self.first_name_label = QLabel("First Name:")
        self.first_name_input = QLineEdit()

        # Last name input field
        self.last_name_label = QLabel("Last Name:")
        self.last_name_input = QLineEdit()

        # Date of birth input field
        self.date_of_birth_label = QLabel("Date of Birth:")
        self.date_of_birth_input = QDateEdit()
        self.date_of_birth_input.setCalendarPopup(True)

        # Gender input field
        self.gender_label = QLabel("Gender:")
        self.gender_input = QComboBox()
        self.gender_input.addItem("Male")
        self.gender_input.addItem("Female")

        # ID input field
        self.id_label = QLabel("ID:")
        self.id_input = QLineEdit()
        self.id_input.setMaxLength(10)  # Set maximum length to 10 characters

        # personal Row
        personal_2_info_layout = QHBoxLayout()
        personal_2_info_layout.addWidget(self.date_of_birth_label)
        personal_2_info_layout.addWidget(self.date_of_birth_input)
        personal_2_info_layout.addWidget(self.gender_label)
        personal_2_info_layout.addWidget(self.gender_input)
        personal_2_info_layout.addWidget(self.id_label)
        personal_2_info_layout.addWidget(self.id_input)

        # Address input field
        self.address_label = QLabel("Address:")
        self.address_input = QLineEdit()

        # Warning field
        self.warning_label = QLabel("Warning:")
        self.warning_input = QLineEdit()

        # Special note field
        self.special_note_label = QLabel("Special Note:")
        self.special_note_input = QLineEdit()

        # Create a layout for the input fields
        layout = QVBoxLayout()

        layout.addWidget(self.first_name_label)
        layout.addWidget(self.first_name_input)
        layout.addWidget(self.last_name_label)
        layout.addWidget(self.last_name_input)
        layout.addLayout(personal_2_info_layout)
        layout.addWidget(self.warning_label)
        layout.addWidget(self.warning_input)
        layout.addWidget(self.special_note_label)
        layout.addWidget(self.special_note_input)

        # Create buttons for save and cancel actions
        save_button = QPushButton("Save")
        cancel_button = QPushButton("Cancel")
        button_layout = QHBoxLayout()
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        # Create a main layout for the dialog
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.exec()

class PreferencesPopup(QDialog):
    def __init__(self, parent=None):
        super(PreferencesPopup, self).__init__(parent)
        self.setWindowTitle("Preferences")

        # Create preference options
        option1_label = QLabel("Option 1:")
        option1_checkbox = QCheckBox()

        option2_label = QLabel("Option 2:")
        option2_checkbox = QCheckBox()

        # Create layout for preference options
        layout = QVBoxLayout()
        layout.addWidget(option1_label)
        layout.addWidget(option1_checkbox)
        layout.addWidget(option2_label)
        layout.addWidget(option2_checkbox)

        # Create buttons for save and cancel actions
        save_button = QPushButton("Save")
        cancel_button = QPushButton("Cancel")
        button_layout = QHBoxLayout()
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        # Create main layout for the dialog
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.exec()


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
        self.preferences_action = QAction("Preferences", self)
        self.preferences_action.triggered.connect(self.open_preferences_popup)

    def create_file_menu(self):
        self.file_menu.addAction(self.create_new_patient_action)
        self.file_menu.addAction(self.look_at_patient_record_action)
        self.file_menu.addAction(self.preferences_action)

    def create_edit_menu(self):
        pass  # Add your actions and submenus for the Edit menu here

    def open_create_patient_popup(self):
        popup = CreatePatientPopup(self)

    def open_preferences_popup(self):
        popup = PreferencesPopup(self)

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

class BackgroundImage:
    def __init__(self, widget):
        self.widget = widget

    def set_image(self, image_path):
        # Create a QLabel to display the image
        image_label = QLabel(self.widget)
        pixmap = QPixmap(image_path)

        # Set the pixmap to the image label
        image_label.setPixmap(pixmap)

        # Set the alignment of the image label to center
        image_label.setAlignment(Qt.AlignCenter)

        # Set the image label as the background of the widget
        palette = QPalette()
        palette.setBrush(QPalette.Background, pixmap)
        self.widget.setPalette(palette)

    def select_image(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Images (*.png *.xpm *.jpg *.bmp)")

        if file_dialog.exec_():
            image_path = file_dialog.selectedFiles()[0]
            self.set_image(image_path)

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        def sx_man_image(tabs):
            image_path = r'C:\Users\nsha2\Documents\python\buttons\M4\imagePAman\sx_pain_Man2.png'
            pixmap = QPixmap(image_path)

            # Resize the image to twice its original size
            resized_pixmap = pixmap.scaled(1227, 700)

            # Create a QLabel to display the image
            image_label = QLabel(tabs)
            image_label.setPixmap(resized_pixmap)
            image_label.setGeometry(650, 0, 1227, 700)

        # setup stylesheet
        apply_stylesheet(app, theme='dark_teal.xml')

        # Create and show your main window
        self.setWindowTitle("Chiropractic SOAP Note Program")
        screen_width = QApplication.desktop().screenGeometry().width()
        screen_height = QApplication.desktop().screenGeometry().height()
        self.setGeometry(-1920, 25, screen_width, screen_height-75)

        # Create a main widget and a vertical layout
        main_widget = QWidget(self)
        layout = QVBoxLayout(main_widget)

        #%%%%%%%%%%%%  Tab stylings
        # # Create the tab widget
        # tab_widget = QTabWidget(main_widget)
        #
        # # Create the tabs
        # settings_tab = QWidget()
        # patient_tab = QWidget()
        # exam_tab = QWidget()
        # daily_notes_tab = QWidget()
        # additional_tab1 = QWidget()
        # additional_tab2 = QWidget()
        #
        # # Add tabs to the tab widget
        # tab_widget.addTab(settings_tab, "Setting")
        # tab_widget.addTab(patient_tab, "Patient Table")
        # tab_widget.addTab(exam_tab, "Exam Table")
        # tab_widget.addTab(daily_notes_tab, "Daily Notes Table")
        # tab_widget.addTab(additional_tab1, "Additional Tab 1")
        # tab_widget.addTab(additional_tab2, "Additional Tab 2")
        #
        # # Create labels for demonstration purposes
        # settings_label = QLabel("This is the Patient Table")
        # patient_label = QLabel("This is the Patient Table")
        # patient_label2 = QLabel("2222his is the Patient Table")
        # exam_label = QLabel("This is the Exam Table")
        # daily_notes_label = QLabel("This is the Daily Notes Table")
        # additional_label1 = QLabel("This is Additional Tab 1")
        # additional_label2 = QLabel("This is Additional Tab 2")
        #
        # # Create layouts for each tab
        # # %%%%%%%%%%  PATIENT TAB
        # patient_layout = QVBoxLayout(patient_tab)
        # patient_layout.addWidget(patient_label)
        # patient_layout.addWidget(patient_label2)
        #
        #
        # # %%%%%%%%%%  EXAM TAB
        # exam_layout = QVBoxLayout(exam_tab)
        # exam_layout.addWidget(exam_label)
        # # Create a QPixmap object from the image file
        # sx_man_image(exam_tab)
        #
        # # %%%%%%%%%%  DAILY NOTES TAB
        # daily_notes_layout = QVBoxLayout(daily_notes_tab)
        # daily_notes_layout.addWidget(daily_notes_label)
        # # Create a QPixmap object from the image file
        # sx_man_image(daily_notes_tab)
        #
        # # %%%%%%%%%%  EXTRA TAB
        # additional_layout1 = QVBoxLayout(additional_tab1)
        # additional_layout1.addWidget(additional_label1)
        #
        # # %%%%%%%%%%  EXTRA TAB
        # additional_layout2 = QVBoxLayout(additional_tab2)
        # additional_layout2.addWidget(additional_label2)
        #
        # # Add the tab widget to the main layout
        # layout.addWidget(tab_widget)

        # Set the main widget
        self.setCentralWidget(main_widget)  #

# %%%%%%%%%%% MENU BAR
        self.create_toolbar()
        self.create_menu_bar()

    def create_menu_bar(self):
        menu_bar = MenuBar(self)
        self.setMenuBar(menu_bar)
    def create_toolbar(self):
        toolbar = ToolBar(self)
        self.addToolBar(toolbar)

    # def create_toolbar(self):
    #     toolbar = QToolBar()
    #     self.addToolBar(toolbar)
    #     toolbar.setIconSize(QSize(32,32))
    #
    #     # Create actions
    #     home_action = QAction(qta.icon('fa5s.home', color='#1de9b6'), "Home", self) # Primary Color dark_teal
    #     home_action.setStatusTip("Go to home")
    #     home_action.triggered.connect(self.home_action_function)
    #
    #     open_action = QAction(qta.icon('fa5s.folder-open', color='red'), "Open", self)
    #     open_action.setStatusTip("Open a directory")
    #     open_action.triggered.connect(self.open_action_function)
    #
    #     refresh_action = QAction(qta.icon('fa5s.sync', color='green'), "Refresh", self)
    #     refresh_action.setStatusTip("Refresh the page")
    #     refresh_action.triggered.connect(self.refresh_action_function)
    #
    #     undo_action = QAction(qta.icon('fa5s.undo', color='yellow'), "Undo", self)
    #     undo_action.setStatusTip("Undo the last action")
    #     undo_action.triggered.connect(self.undo_action_function)
    #
    #     redo_action = QAction(qta.icon('fa5s.redo', color='purple'), "Redo", self)
    #     redo_action.setStatusTip("Redo the last action")
    #     redo_action.triggered.connect(self.redo_action_function)
    #
    #         # Add actions to the toolbar
    #     toolbar.addAction(home_action)
    #     toolbar.addAction(open_action)
    #     toolbar.addAction(refresh_action)
    #     toolbar.addAction(undo_action)
    #     toolbar.addAction(redo_action)
    #
    # def home_action_function(self):
    #     # Handle the action when the home icon is clicked
    #     print("Home icon action triggered")
    #
    # def open_action_function(self):
    #     # Handle the action when the open icon is clicked
    #     print("Open icon action triggered")
    #
    # def refresh_action_function(self):
    #     # Handle the action when the refresh icon is clicked
    #     print("Refresh icon action triggered")
    #
    # def undo_action_function(self):
    #     # Handle the action when the undo icon is clicked
    #     print("Undo icon action triggered")
    #
    # def redo_action_function(self):
    #     # Handle the action when the redo icon is clicked
    #     print("Redo icon action triggered")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
