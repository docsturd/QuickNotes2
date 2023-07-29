from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Load preferences
        self.load_settings()

        # Create and show your main window
        self.setWindowTitle("Chiropractic SOAP Note Program")
        screen_width = QApplication.desktop().screenGeometry().width()
        screen_height = QApplication.desktop().screenGeometry().height()
        self.setGeometry(-1920, 25, screen_width, screen_height-75)

        # Create a main widget and a vertical layout
        main_widget = QWidget(self)
        layout = QVBoxLayout(main_widget)

        # Set the main widget
        self.setCentralWidget(main_widget)

        # Set the background image
        self.set_background_image('path/to/your/image.jpg')

        # MENU BAR
        self.create_toolbar()
        self.create_menu_bar()

    def set_background_image(self, image_path):
        # Create a QPixmap from the image file
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            # Scale the pixmap to the size of the main window
            scaled_pixmap = pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            # Set the background image using stylesheet
            self.setStyleSheet(f"background-image: url({scaled_pixmap.toImage().format().data()});")

    def load_settings(self):
        try:
            if os.path.exists('settings.json'):
                with open('settings.json', 'r') as f:
                    prefs = json.load(f)

                theme = prefs.get('theme')
                if theme:
                    apply_stylesheet(self, theme=theme)
        except Exception as e:
            print(f"Failed to load preferences: {e}")

    # Load other preferences here as needed

    def create_menu_bar(self):
        menu_bar = MenuBar(self)
        self.setMenuBar(menu_bar)

    def create_toolbar(self):
        toolbar = ToolBar(self)
        self.addToolBar(toolbar)
