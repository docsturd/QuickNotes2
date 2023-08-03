from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from utils.layout_tools import *


handedness = [
    "right", "left", "ambidextrous"
]

biometrics = [
    "pulse", "Height", "Weight", "POX"
]  #add radio button Handeness

review_of_systems_pos = [
    "vision \u25B3 +",  "hearing \u25B3 +", "hair or nails \u25B3 +", "fever +", "vertigo +",
    "sore throat +", "nasal congestion +", "nosebleeds +", "chest pain  +",
    "Shortness of breath +", "nausea +","vomiting +", "diarrhea  +",
    "constipation +", "abdominal pain +", "dysuria +", "rash +", "itching +",
    "anxiety +", "depression +", "stress +"
]

gen_objective = [
    f"GEN:\nNo Apparent Distress",
    "HEENT:\nNormocephalic Atraumatic",
    "RESP:\nUnlabored",
    "PSYCH:\nNormal Mood/Affect",
    "APPEARANCE:\nWell Groomed",
    "NEURO:\nAlert/Relaxed/Cooperative/\nCoherent/Person/Place/Time. \nA Detailed Cognitive test not performed",
]
# Fixated, hypertonic, Tender, Inflamation, right, left
area_observation_objective = {
    "Cervical": ["F", "H", "T", "I", "Rt", "Lt"], "Thoracic": ["F", "H", "T", "I", "Rt", "Lt"],
    "Lumbar": ["F", "H", "T", "I", "Rt", "Lt"], "Sacroiliac": ["F", "H", "T", "I", "Rt", "Lt"],
    "Shoulder": ["F", "H", "T", "I", "Rt", "Lt"], "Hip": ["F", "H", "T", "I", "Rt", "Lt"]
}
extremities_observation_objective = {
    "Elbow": ["F", "H", "T", "I", "Rt", "Lt"], "Wrist": ["F", "H", "T", "I", "Rt", "Lt"], "Hand": ["F", "H", "T", "I", "Rt", "Lt"],
    "Knee": ["F", "H", "T", "I", "Rt", "Lt"], "Ankle": ["F", "H", "T", "I", "Rt", "Lt"], "Foot": ["F", "H", "T", "I", "Rt", "Lt"],
}

above_buttons = [
    "Health History",
    "Observation",
    "Palpation",
    "Range of Motion (ROM) Assessment",
    "Orthopedic Tests",
    "Neurological Assessment",
    "X-rays or Imaging",
    "Surface Electromyography (sEMG)",
    "Thermography",
    "Postural Analysis",
    "Functional Movement Assessment",
    "Gait Analysis",
]
def create_above_buttons(self):
    # Create buttons using 'above_buttons' variable for naming
    above_buttons_layout = QGridLayout()
    cols = 3
    rows = 5
    for i, btn_name in enumerate(self.above_buttons):
        button = QPushButton(btn_name)
        row, col = divmod(i, rows)
        above_buttons_layout.addWidget(button, row, col)
    return above_buttons_layout

def create_radiobuttons_layout(title, items, items_per_row=1):
    """Create a layout with radio buttons.
    Parameters:
    - buttons_list (list): A list of strings, each string will be a label for a radio button.
    - items_per_row (int, optional): The number of radio buttons per row. Default is 1.
    Returns:
    - QGridLayout: A layout with radio buttons.
    """
    layout = QGridLayout()
    row = 0
    if title:
        layout.addWidget(QLabel(title), 0, 0, 1, -1)  # Span across all columns
        row += 1  # Increment the row so that radio buttons start from next row

    # Keeping track of which row and column we are placing items
    col = 0

    # Add each radio button to the grid layout
    for item in items:
        radiobtn = QRadioButton(item)
        layout.addWidget(radiobtn, row, col * 2 + 1)

        # Move to next column and check if we need to wrap to next row
        col += 1
        if col >= items_per_row:
            col = 0
            row += 1

    wrapper_widget = QWidget()
    wrapper_widget.setLayout(layout)
    return wrapper_widget

def create_groupbox_with_lineedit(items, items_per_row=1):
    """Create a group box with form layout for biometrics.

    Parameters:
    - items (list): List of items for biometric fields.
    - items_per_row (int, optional): The number of items per row. Default is 1.

    Returns:
    - QGroupBox: A group box with form layout.
    """
    groupbox = QGroupBox("Biometrics")
    layout = QGridLayout()

    # Keeping track of which row and column we are placing items
    row, col = 0, 0

    # Create QLineEdit for each item and add to the grid layout
    for item in items:
        layout.addWidget(QLabel(item), row, col * 2)  # Multiply col by 2 for item and QLineEdit pair
        layout.addWidget(QLineEdit(), row, col * 2 + 1)

        # Move to next column and check if we need to wrap to next row
        col += 1
        if col >= items_per_row:
            col = 0
            row += 1

    groupbox.setLayout(layout)
    return groupbox

def create_groupbox_with_checkboxes(title, items, items_per_row):
    """Create a group box with checkboxes.
    Parameters:
    - title (str): The title for the group box.
    - items (list): A list of strings, each string will be a label for a checkbox.
    - items_per_row (int, optional): The number of checkboxes per row. Default is 5.
    Returns:
    - QGroupBox: A group box with checkboxes.
    """
    groupbox = QGroupBox(title)
    layout = QGridLayout()

    # Keeping track of which row and column we are placing items
    row, col = 0, 0

    for item in items:
        checkbox = QCheckBox(item)
        layout.addWidget(checkbox, row, col)

        # Move to next column and check if we need to wrap to next row
        col += 1
        if col >= items_per_row:
            col = 0
            row += 1

    groupbox.setLayout(layout)
    return groupbox

def create_dictionary_checkbox_form(title, categories_and_options, items_per_row=2):
    """Create a group box with a form of checkboxes based on a dictionary.
    Parameters:
    - title (str): The title of the group box.
    - categories_and_options (dict): A dictionary where keys are categories and values are lists of options.
    - items_per_row (int, optional): The number of categories per row. Default is 2.
    Returns:
    - QGroupBox: A group box with the form.
    """
    group_box = QGroupBox(title)
    layout = QVBoxLayout()

    # Create a grid layout for the category headers (labels)
    header_layout = QHBoxLayout()
    for category in categories_and_options.keys():
        label = QLabel(category)
        header_layout.addWidget(label)
    layout.addLayout(header_layout)

    # Create the checkboxes for each category and option
    max_options = max(len(options) for options in categories_and_options.values())
    for i in range(max_options):
        option_layout = QHBoxLayout()
        for options in categories_and_options.values():
            if i < len(options):
                checkbox = QCheckBox(options[i])
                option_layout.addWidget(checkbox)
            else:
                # If no option, just add a placeholder to keep alignment
                option_layout.addWidget(QLabel(""))
        layout.addLayout(option_layout)

    group_box.setLayout(layout)
    return group_box



# Updating the Objective class to include the group boxes
class Objective(QWidget):
    text_to_append = pyqtSignal(str)
    update_output = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Objective, self).__init__(parent)

        main_layout = QVBoxLayout(self)      # Main vertical layout
        layout = QHBoxLayout()               # Horizontal layout for group boxes
        main_layout.addLayout(layout)        # Add horizontal layout to main vertical layout

        # Adding the group boxes
        biometrics_groupbox = create_groupbox_with_lineedit(biometrics, 1)
        biometrics_handedness = create_radiobuttons_layout("Handedness", handedness, 3)
        review_of_systems_groupbox = create_groupbox_with_checkboxes("Review Of Systems", review_of_systems_pos, 3)
        gen_objective_groupbox = create_groupbox_with_checkboxes("General Objective", gen_objective, 1)
        regional_objective = create_dictionary_checkbox_form("General Observation", area_observation_objective, 1)


        layout.addWidget(biometrics_groupbox)
        main_layout.addWidget(biometrics_handedness)
        layout.addWidget(review_of_systems_groupbox)
        layout.addWidget(gen_objective_groupbox)
        layout.addWidget(regional_objective)

        # Adding the Biometrics group box
        # biometrics_groupbox = create_groupbox_with_lineedit(biometrics, 2)
        # main_layout.addWidget(biometrics_groupbox)

        self.setLayout(main_layout)
