import time
import json

class TextCreator:
    def __init__(self, output_file, full_name, address_parts, settings_file='settings.json'):
        self.output_file = output_file
        self.full_name = full_name
        self.address_parts = address_parts
        self.story = []

        # Read the settings from the JSON file
        with open(settings_file) as file:
            self.settings = json.load(file)

    def create_document(self):
        self.add_time()
        self.add_address(self.full_name, self.address_parts)
        self.add_greeting(self.full_name.split()[0].strip())
        self.add_subjective()
        self.add_objective()
        self.add_assesment()
        self.add_plan()
        self.add_salutation()
        self.build()

    def add_time(self):
        ptext = '%s\n\n' % time.ctime()
        self.story.append(ptext)

    def add_address(self, full_name, address_parts):
        ptext = '%s\n\n' % full_name
        self.story.append(ptext)
        for part in address_parts:
            ptext = '%s\n' % part.strip()
            self.story.append(ptext)

    def add_greeting(self, name):
        ptext = 'Dear %s:\n' % name
        self.story.append(ptext)

    def add_subjective(self):
        title = 'SUBJECTIVE:\n'
        self.story.append(title)
        ptext = 'We would like to welcome you to our subscriber base for Pythonista Magazine! You will receive 12 issues at the excellent introductory price of $99.00. Please respond by 03/05/2010 to start receiving your subscription and get the following free gift: tin foil hat.\n'
        self.story.append(ptext)

    def add_objective(self):
        title = 'OBJECTIVE:\n'
        self.story.append(title)
        ptext = 'All good men new paragraph\n'
        self.story.append(ptext)

    def add_assesment(self):
        title = 'ASSESSMENT:\n'
        self.story.append(title)
        ptext = 'All good men new paragraph\n'
        self.story.append(ptext)

    def add_plan(self):
        title = 'PLAN:\n'
        self.story.append(title)
        ptext = 'All good men new paragraph\n'
        self.story.append(ptext)

    def add_salutation(self):
        ptext = 'Thank you very much and we look forward to serving you.\n'
        self.story.append(ptext)
        ptext = 'Sincerely,\n'
        self.story.append(ptext)
        ptext = self.settings['provider_name'] + '\n'
        self.story.append(ptext)
        ptext = "{}\n{}  -  {}, {} {}  -  {}\n".format(self.settings['business_info'], self.settings['business_address'], self.settings['city'], self.settings['st'], self.settings['zip'], self.settings['phone_number'])
        self.story.append(ptext)

    def build(self):
        with open(self.output_file, 'w') as f:
            f.write(''.join(self.story))

# Load the settings
with open('settings.json') as file:
    settings = json.load(file)

text_creator = TextCreator(
    output_file = "SAMPLE_doc.txt",
    full_name = "Mike Driscoll",
    address_parts = ["411 State St.", "Marshalltown, IA 50158"],
    settings_file='settings.json'
)
text_creator.create_document()
