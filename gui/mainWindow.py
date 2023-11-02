from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QAction, QIcon

from gui.windows.сontentWindow import ContentWindow

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()

        open_button = QPushButton(icon=QIcon('icons/folder-open.png'))
        open_button.setToolTip("Open file")
        open_button.clicked.connect(self.open_content_window)


        filter_button = QPushButton(icon=QIcon('icons/settings-sliders.png'))
        filter_button.setToolTip("Filters")


        layout.addWidget(open_button)
        layout.addWidget(filter_button)
        
        self.setLayout(layout)

        self.setWindowTitle('IVP')
        self.show()

    def open_content_window(self):
        self.content_screen = ContentWindow()
        self.content_screen.show()