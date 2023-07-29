from reportlab.lib.pagesizes import *#letter
from reportlab.platypus import *#SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import *#getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import *#TA_JUSTIFY
from reportlab.lib.units import *#inch
# import time
import json

# Then, throughout the rest of your code, replace `PDFCreator.setting_name` with `self.settings['setting_name']`.

class PDFCreator:
    def __init__(self, output_file, logo, full_name, address_parts, settings_file='settings.json'):
        self.output_file = output_file
        self.logo = logo
        self.full_name = full_name
        self.address_parts = address_parts
        self.story = []

        # Read the settings from the JSON file
        with open(settings_file) as file:
            self.settings = json.load(file)

        # Define styles
        self.styles = getSampleStyleSheet()
        self.heading1_style = self.styles["Heading1"]
        self.heading1_style.fontSize = 18
        self.heading1_style.underline = True
        self.heading1_style.alignment = TA_CENTER

        self.normal_style = self.styles["Normal"]
        self.normal_style.fontSize = 8

        self.title_style = self.styles["Normal"].clone('normal_style')
        self.title_style.fontSize = 8

        self.text_style = self.styles["Normal"].clone('text_style')
        self.text_style.fontSize = 8
        self.text_style.leftIndent = 16  # This is the indentation (change to the value you want)
        self.text_style.alignment = TA_JUSTIFY
        self.center_style = self.styles["Normal"].clone('center_style')
        self.center_style.alignment = TA_CENTER

    def create_document(self):
        # self.add_image(1, 1)
        self.add_header()
        self.add_time()
        self.add_address(self.full_name, self.address_parts)
        # self.add_greeting(self.full_name.split()[0].strip())
        self.add_subjective()
        self.add_objective()
        self.add_assesment()
        self.add_plan()
        self.add_salutation()
        self.build()

    def add_image(self, width, height):
        im = Image(self.logo, width * inch, height * inch)
        self.story.append(im)
    def add_header(self):
        ptext = 'Soap Note'
        self.story.append(Paragraph(ptext, self.heading1_style))
        self.story.append(Spacer(1, 6))
    def add_time(self):
        from datetime import datetime
        now = datetime.now()
        formatted_time = now.strftime("%m/%d/%Y, %H:%M")
        ptext = '%s' % formatted_time
        self.story.append(Paragraph(ptext, self.normal_style))
        self.story.append(Spacer(1, 3))

    def add_address(self, full_name, address_parts):
        ptext = '%s' % full_name
        self.story.append(Paragraph(ptext, self.normal_style))
        for part in address_parts:
            ptext = '%s' % part.strip()
            self.story.append(Paragraph(ptext, self.normal_style))
        self.story.append(Spacer(1, 12))



    def add_subjective(self):
        # Add the title to the story
        ptext = 'SUBJECTIVE:'
        self.story.append(Paragraph(ptext, self.normal_style))
        # Add the text to the story
        ptext = 'We would like to welcome you to our subscriber base for Pythonista Magazine! You will receive 12 issues at the excellent introductory price of $99.00. Please respond by 03/05/2010 to start receiving your subscription and get the following free gift: tin foil hat.'
        self.story.append(Paragraph(ptext, self.text_style))
        self.story.append(Spacer(1, 3))
    def add_objective(self):
        # Add the title to the story
        title = 'OBJECTIVE:'
        self.story.append(Paragraph(title, self.normal_style))
        # Add the text to the story
        ptext = 'All good men new paragraph'
        self.story.append(Paragraph(ptext, self.text_style))
        self.story.append(Spacer(1, 3))
    def add_assesment(self):
        # Add the title to the story
        title = 'ASSESSMENT:'
        self.story.append(Paragraph(title, self.normal_style))
        # Add the text to the story
        ptext = 'All good men new paragraph'
        self.story.append(Paragraph(ptext, self.text_style))
        self.story.append(Spacer(1, 3))
    def add_plan(self):
        title = 'PLAN:'
        self.story.append(Paragraph(title, self.normal_style))
        # Add the text to the story
        ptext = 'All good men new paragraph'
        self.story.append(Paragraph(ptext, self.text_style))
        self.story.append(Spacer(1, 3))

    def add_salutation(self):
        ptext = 'Thank you very much and we look forward to serving you.'
        self.story.append(Paragraph(ptext, self.normal_style))
        self.story.append(Spacer(1, 12))

        ptext = 'Sincerely,'
        self.story.append(Paragraph(ptext, self.normal_style))
        self.story.append(Spacer(1, 12))

        # Add provider name from settings
        ptext = self.settings['provider_name']
        self.story.append(Paragraph(ptext, self.normal_style))
        self.story.append(Spacer(1, 12))

        # Add business Info from settings
        ptext = f"{self.settings['business_info']}<br/>{self.settings['business_address']}  -  {self.settings['city']}, {self.settings['st']} {self.settings['zip']}  -  {self.settings['phone_number']}"
        self.story.append(Paragraph(ptext, self.center_style))
        self.story.append(Spacer(1, 12))

    def build(self):
        custom_page_size = (8.5 * inch, 8.5 * inch)
        doc = SimpleDocTemplate(self.output_file, pagesize=custom_page_size, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
        doc.build(self.story)

# pdf_creator = PDFCreator("SAMPLE_doc_reportlab.pdf", PDFCreator.settings['business_logo'], "Mike Driscoll", ["411 State St.", "Marshalltown, IA 50158"])
# pdf_creator.create_document()
# Load the settings
with open('settings.json') as file:
    settings = json.load(file)

pdf_creator = PDFCreator(
    output_file = "SAMPLE_doc_reportlab.pdf",
    logo = settings['business_logo'],
    full_name = "Mike Driscoll",
    address_parts = ["pretend ID", "warning", "special_note"],
    settings_file='settings.json'
)
pdf_creator.create_document()
