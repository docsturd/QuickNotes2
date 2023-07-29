from reportlab.lib.pagesizes import *#letter
from reportlab.platypus import *#SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import *#getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import *#TA_JUSTIFY
from reportlab.lib.units import *#inch
import time
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

    def create_document(self):
        self.add_image(1, 1)
        self.add_time()
        self.add_address(self.full_name, self.address_parts)
        self.add_greeting(self.full_name.split()[0].strip())
        self.add_subjective()
        self.add_objective()
        self.add_assesment()
        self.add_plan()
        self.add_salutation()
        self.build()

    def add_image(self, width, height):
        im = Image(self.logo, width * inch, height * inch)
        self.story.append(im)

    def add_time(self):
        styles = getSampleStyleSheet()
        ptext = '%s' % time.ctime()
        self.story.append(Paragraph(ptext, styles["Normal"]))
        self.story.append(Spacer(1, 12))

    def add_address(self, full_name, address_parts):
        styles = getSampleStyleSheet()
        ptext = '%s' % full_name
        self.story.append(Paragraph(ptext, styles["Normal"]))
        for part in address_parts:
            ptext = '%s' % part.strip()
            self.story.append(Paragraph(ptext, styles["Normal"]))
        self.story.append(Spacer(1, 12))

    def add_greeting(self, name):
        styles = getSampleStyleSheet()
        ptext = 'Dear %s:' % name
        self.story.append(Paragraph(ptext, styles["Normal"]))
        self.story.append(Spacer(1, 12))

    def add_subjective(self):
        styles = getSampleStyleSheet()

        # Create a new style for the title
        title_style = styles["Normal"].clone('title_style')
        title_style.fontName = 'Helvetica-Bold'
        title_style.fontSize = 10

        # Add the title to the story
        title = 'SUBJECTIVE:'
        self.story.append(Paragraph(title, title_style))
        # self.story.append(Spacer(1, 0))

        # Create a new style for the indented and justified text
        text_style = styles["BodyText"].clone('text_style')
        text_style.leftIndent = 9  # This is the indentation (change to the value you want)
        text_style.alignment = TA_JUSTIFY

        # Add the text to the story
        ptext = 'We would like to welcome you to our subscriber base for Pythonista Magazine! You will receive 12 issues at the excellent introductory price of $99.00. Please respond by 03/05/2010 to start receiving your subscription and get the following free gift: tin foil hat.'
        self.story.append(Paragraph(ptext, text_style))
        self.story.append(Spacer(1, 12))
    def add_objective(self):
        styles = getSampleStyleSheet()

        # Create a new style for the title
        title_style = styles["Normal"].clone('title_style')
        title_style.fontName = 'Helvetica-Bold'
        title_style.fontSize = 10

        # Add the title to the story
        title = 'OBJECTIVE:'
        self.story.append(Paragraph(title, title_style))
        # self.story.append(Spacer(1, 0))

        # Create a new style for the indented and justified text
        text_style = styles["BodyText"].clone('text_style')
        text_style.leftIndent = 9  # This is the indentation (change to the value you want)
        text_style.alignment = TA_JUSTIFY

        # Add the text to the story
        ptext = 'All good men new paragraph'
        self.story.append(Paragraph(ptext, text_style))
        self.story.append(Spacer(1, 12))
    def add_assesment(self):
        styles = getSampleStyleSheet()

        # Create a new style for the title
        title_style = styles["Normal"].clone('title_style')
        title_style.fontName = 'Helvetica-Bold'
        title_style.fontSize = 10

        # Add the title to the story
        title = 'ASSESSMENT:'
        self.story.append(Paragraph(title, title_style))
        # self.story.append(Spacer(1, 0))

        # Create a new style for the indented and justified text
        text_style = styles["BodyText"].clone('text_style')
        text_style.leftIndent = 9  # This is the indentation (change to the value you want)
        text_style.alignment = TA_JUSTIFY

        # Add the text to the story
        ptext = 'All good men new paragraph'
        self.story.append(Paragraph(ptext, text_style))
        self.story.append(Spacer(1, 12))
    def add_plan(self):
        styles = getSampleStyleSheet()

        # Create a new style for the title
        title_style = styles["Normal"].clone('title_style')
        title_style.fontName = 'Helvetica-Bold'
        title_style.fontSize = 10

        # Add the title to the story
        title = 'PLAN:'
        self.story.append(Paragraph(title, title_style))
        # self.story.append(Spacer(1, 0))

        # Create a new style for the indented and justified text
        text_style = styles["BodyText"].clone('text_style')
        text_style.leftIndent = 9  # This is the indentation (change to the value you want)
        text_style.alignment = TA_JUSTIFY

        # Add the text to the story
        ptext = 'All good men new paragraph'
        self.story.append(Paragraph(ptext, text_style))
        self.story.append(Spacer(1, 12))

    def add_salutation(self):
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        styles.add(ParagraphStyle(name='Center', alignment=1)) # 1 is the code for TA_CENTER

        # Define the salutation text
        ptext = 'Thank you very much and we look forward to serving you.'
        self.story.append(Paragraph(ptext, styles["Justify"]))
        self.story.append(Spacer(1, 12))

        ptext = 'Sincerely,'
        self.story.append(Paragraph(ptext, styles["Normal"]))
        self.story.append(Spacer(1, 12))

        # Add provider name from settings
        ptext = self.settings['provider_name']
        self.story.append(Paragraph(ptext, styles["Normal"]))
        self.story.append(Spacer(1, 12))

        # Add business Info from settings
        ptext = f"{self.settings['business_info']}<br/>{self.settings['business_address']}  -  {self.settings['city']}, {self.settings['st']} {self.settings['zip']}  -  {self.settings['phone_number']}"
        self.story.append(Paragraph(ptext, styles["Center"]))
        self.story.append(Spacer(1, 12))

    def build(self):
        doc = SimpleDocTemplate(self.output_file, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
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
    address_parts = ["411 State St.", "Marshalltown, IA 50158"],
    settings_file='settings.json'
)
pdf_creator.create_document()
