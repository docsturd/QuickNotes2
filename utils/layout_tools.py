from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


def create_horizontal_line_with_spacer():
    """
    Create a QVBoxLayout that contains a horizontal line and a spacer.

    Returns:
        QVBoxLayout: A layout containing a horizontal line and a spacer.
    """
    layout = QVBoxLayout()

    # Creating the horizontal line (QFrame)
    hline = QFrame()
    hline.setFrameShape(QFrame.HLine)
    hline.setFrameShadow(QFrame.Sunken)
    layout.addWidget(hline)

    # Adding the spacer
    spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
    layout.addItem(spacer)

    return layout

def create_buttons(layout, padding, columns, rows, items):
    """
    Create a grid of buttons and add them to the provided layout.

    Parameters:
    - layout (QGridLayout): The layout to which the buttons will be added.
    - padding (int): Spacing between the buttons.
    - columns (int): Number of columns in the grid.
    - rows (int): Number of rows in the grid.
    - items (List[str]): A list of names/labels for the buttons.

    Notes:
    - The total number of buttons created will be columns x rows.
    - If the number of items provided is less than columns x rows,
      the function will create only as many buttons as there are items.
    - Button dimensions are fixed to a height of 100 and a width of 300.

    Returns:
    None. The buttons are added directly to the provided layout.
    """
    layout.setSpacing(padding)  # Adding spacing between buttons

    # Create buttons, grouped in the specified rows and columns.
    for i in range(columns):  # for each column
        for j in range(rows):  # for each button in the column
            index = i * rows + j
            if index < len(items):  # Ensure we don't go out of bounds of the items list
                button_name = items[index]
                button = QPushButton(button_name)
                button.setFixedHeight(100)  # Setting the height of the button
                button.setFixedWidth(300)  # Setting the width of the button
                layout.addWidget(button, j, i)

def create_groupbox_with_checkboxes(title, items, items_per_row=5):
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

    # Add "Append" and "Cancel" buttons to the bottom
    append_button = QPushButton("Append")
    cancel_button = QPushButton("Cancel")

    # Note: Here we are placing the buttons in the next row after the checkboxes.
    # You can adjust the column index if needed.
    layout.addWidget(append_button, row + 1, 0)
    layout.addWidget(cancel_button, row + 1, 1)

    # TODO: Connect the buttons to the desired slots (functions) if needed
    # append_button.clicked.connect(some_function)
    # cancel_button.clicked.connect(some_other_function)

    groupbox.setLayout(layout)
    return groupbox
