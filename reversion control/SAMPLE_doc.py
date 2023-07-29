from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.units import inch
import time
import json



class PDFCreator:
    # Read the settings from the JSON file
    with open('settings.json') as file:
        settings = json.load(file)

    # Extract the values from the settings dictionary
    theme = settings['theme']
    business_info = settings['business_info']
    business_logo = settings['business_logo']
    business_address = settings['business_address']
    city = settings['city']
    state = settings['st']
    zip_code = settings['zip']
    provider_name = settings['provider_name']
    phone_number = settings['phone_number']

    def __init__(self, output_file, logo, full_name, address_parts):
        self.output_file = output_file
        self.logo = logo
        self.full_name = full_name
        self.address_parts = address_parts
        self.story = []

    def create_document(self):
        self.add_image(1, 1)
        self.add_time()
        self.add_address(self.full_name, self.address_parts)
        self.add_greeting(self.full_name.split()[0].strip())
        self.add_body()
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

    def add_body(self):
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        ptext = 'We would like to welcome you to our subscriber base for Pythonista Magazine! You will receive 12 issues at the excellent introductory price of $99.00. Please respond by 03/05/2010 to start receiving your subscription and get the following free gift: tin foil hat.'
        self.story.append(Paragraph(ptext, styles["Justify"]))
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
        ptext = PDFCreator.provider_name
        self.story.append(Paragraph(ptext, styles["Normal"]))
        self.story.append(Spacer(1, 12))

        # Add business Info from settings
        ptext = f"{PDFCreator.business_info}<br/>{PDFCreator.business_address}  *  {PDFCreator.city}, {PDFCreator.state} {PDFCreator.zip_code}  *  {PDFCreator.phone_number}"
        self.story.append(Paragraph(ptext, styles["Center"]))
        self.story.append(Spacer(1, 12))

    def build(self):
        doc = SimpleDocTemplate(self.output_file, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        doc.build(self.story)

pdf_creator = PDFCreator("SAMPLE_doc_reportlab.pdf", PDFCreator.settings['business_logo'], "Mike Driscoll", ["411 State St.", "Marshalltown, IA 50158"])
pdf_creator.create_document()
