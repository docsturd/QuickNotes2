from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from utils.layout_tools import *
from Objective.ObjectiveFunctions import *


handedness = [
    "right", "left", "ambidextrous"
]


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

objective_buttons = [
    "BioMetric",
    "Observation",
    "Palpation",
    "Range of Motion Assessment",
    "Orthopedic Tests",
    "Neurological Assessment",
    "Xrays or Imaging",
    "Surface Electromyography",
    "Thermography",
    "Postural Analysis",
    "Functional Movement Assessment",
    "Gait Analysis", "place13", "place14", "place 15"
]

class Objective(QWidget):
    text_to_append = pyqtSignal(str)
    update_output = pyqtSignal(str)
    

            
    def __init__(self, parent=None):
        super(Objective, self).__init__(parent)

        layout = QGridLayout()
        # create_buttons Called from utils.layout_tools
        create_buttons(layout, 40, 3, 5, objective_buttons)
        
        # Retrieve buttons from the layout
        buttons = self.get_buttons_from_layout(layout)
        
        # Connect each button's clicked signal to the button_clicked function
        for btn in buttons:
            btn.clicked.connect(self.button_clicked)

        self.setLayout(layout)
    
    def button_clicked(self):
        button = QApplication.instance().sender()
        if button:
            if button.text() == "Biometric":
                self.open_biometric_window()
            elif button.text() == "Observation":
                self.open_observation_window()
    
    def open_observation_window(self):
        import subprocess
        process = subprocess.Popen(["python", "C:\\Users\\user\\Documents\\QuickNotes2\\Objective\\observation.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if stdout:
            print("Output:", stdout.decode())
        if stderr:
            print("Error:", stderr.decode())
            
    def get_buttons_from_layout(self, layout):
        buttons = []
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if isinstance(widget, QPushButton):
                buttons.append(widget)
        return buttons