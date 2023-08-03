from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from utils.layout_tools import create_horizontal_line_with_spacer

review_of_systems_pos = [
    "fever +", "vision \u25B3 +", "earache +", "vertigo +", "hearing \u25B3 +",
    "sore throat +", "nasal congestion +", "nosebleeds +", "chest pain  +",
    "Shortness of breath +", "nausea +","vomiting +", "diarrhea  +",
    "constipation +", "abdominal pain +", "dysuria +", "rash +", "itching +", "\u25B3 hair or nails +",
    "anxiety +", "depression +", "stress +"
]

gen_objective = [
    f"GENERAL:\nNo Apparent Distress",
    "HEENT:\nNormocephalic Atraumatic",
    "RESPIRTORY:\nUnlabored",
    "PSYCHIATRIC:\nNormal Mood/Affect",
    "APPEARANCE:\nWell Groomed",
    "NEUROLOGICAL:\nAlert/Relaxed/Cooperative/Coherent/Person/Place/Time. A Detailed Cognitive test not performed",
]
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
# Updating the Objective class to include the group boxes
class Objective(QWidget):
    text_to_append = pyqtSignal(str)
    update_output = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Objective, self).__init__(parent)
        layout = QVBoxLayout(self)

        # Adding the group boxes
        review_of_systems_groupbox = create_groupbox_with_checkboxes("gen_objective", review_of_systems_pos, 2)
        gen_objective_groupbox = create_groupbox_with_checkboxes("gen_objective", gen_objective, 2)

        layout.addWidget(review_of_systems_groupbox)
        layout.addWidget(gen_objective_groupbox)

        self.setLayout(layout)
