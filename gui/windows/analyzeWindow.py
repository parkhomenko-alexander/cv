from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt6.QtGui import QPixmap, QImage, QAction
from PyQt6.QtCore import QTimer, Qt, pyqtSignal

from gui.config import config

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import cv2


class AnalyzeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.screen_w = config.screen_w
        self.screen_h = config.screen_h


        self.histogram_label = QLabel(self)
        
        
        self.main_layout = QGridLayout()
        self.initUI()

    def initUI(self):
        super().__init__()
        
        self.setWindowTitle('Statistics')
        self.setGeometry(600, 200, self.screen_w, self.screen_h)

        self.setLayout(self.main_layout)

    def convert_cv_to_pixmap(self, image):
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        return pixmap
    
    def display_params(self, hist):
        print(hist)
        # hist = cv2.imread(name)
        self.histogram_label.setPixmap(self.convert_cv_to_pixmap(hist))
        self.main_layout.addWidget(self.histogram_label, 0, 0, 1, 1)