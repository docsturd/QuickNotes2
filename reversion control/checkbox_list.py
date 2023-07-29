
# class Subjective:
#     def __init__(self):
        # ... your other initialization code ...
        self.interfers = {} # create a dictionary to store interfers

    # ... rest of your methods ...



# def create_group_box(self, title, symptoms):
     # ... your other create_group_box code ...
# interfer
        interfer_groupbox = QGroupBox("interfer")
        interfer_vbox = QVBoxLayout()

        interfers_list = interfer_list = ["Work", "Sleep", "Travel", "Bathing", "Tolileting", "Preparing food", "Eating", "Walking", "Exercising", "Sleeping", "Dressing", "Tying Shoes", "Work"]
        interfers_list = [interfer.lower() for interfer in interfers_list]
        interfers_list.sort()

        MAX_ITEMS_PER_ROW = 2
        item_counter = 0
        hbox_interfers = QHBoxLayout()

        for interfer in interfers_list:
            if item_counter >= MAX_ITEMS_PER_ROW:
                interfer_vbox.addLayout(hbox_interfers)  # <- This line is changed
                hbox_interfers = QHBoxLayout()
                item_counter = 0

            checkbox = QCheckBox(interfer)
            checkbox.stateChanged.connect(lambda state, checkbox=checkbox: self.set_interfer(checkbox.text(), state))
            hbox_interfers.addWidget(checkbox)
            item_counter += 1

        if hbox_interfers.count() > 0:  # add remaining checkboxes if any
            interfer_vbox.addLayout(hbox_interfers)  # <- This line is changed too

        interfer_groupbox.setLayout(interfer_vbox)
        main_hbox.addWidget(interfer_groupbox)  #
# def symptom_emit_text(self, symptom, pain_severity, title)
 # ... your other symptom_emit_text code ...
# interfer
        checked_interfers = [comp for comp, checked in self.interfers.items() if checked]
        if checked_interfers:
            interfer_text = ", ".join(checked_interfers[:-1])
            if len(checked_interfers) > 1:
                interfer_text += f" and {checked_interfers[-1]}"
            else:
                interfer_text = checked_interfers[0]
            interfer_text = f"interfer of: {interfer_text}."
        else:
            interfer_text = ""

def set_interfer(self, interfer, state):
    self.interfers[interfer] = state == Qt.Checked
