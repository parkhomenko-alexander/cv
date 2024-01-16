from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QTextBrowser, QTextEdit
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

        statistics_h, statistics_w = 100, 100
        self.means_label = QTextEdit(self)
        self.means_label.setReadOnly(True)  
        self.means_label.setFixedHeight(statistics_h)
        self.means_label.setFixedWidth(statistics_w)

        self.variance_label = QTextEdit(self)
        self.variance_label.setReadOnly(True)  
        self.variance_label.setFixedHeight(statistics_h)
        self.variance_label.setFixedWidth(statistics_w)

        self.std_label = QTextEdit(self)
        self.std_label.setReadOnly(True)  
        self.std_label.setFixedHeight(statistics_h)
        self.std_label.setFixedWidth(statistics_w)

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
    
    def display_params(self, hist, means, variance, std):

        text = "Среднее:\n"
        for m in means:
            text += f'''   {m["name"]}: {m["val"]}\n'''
        self.means_label.setPlainText(text)
        
        text = ""
        text += "Дисперсия:\n"
        for v in variance:
            text += f'''   {v["name"]}: {v["val"]}\n'''        
        self.variance_label.setPlainText(text)

        text = ""
        text += "Стд отклонение:\n"
        for v in std:
            text += f'''   {v["name"]}: {v["val"]}\n'''        
        self.std_label.setPlainText(text)


        self.histogram_label.setPixmap(self.convert_cv_to_pixmap(hist))

        self.main_layout.setSpacing(0)

        
        self.main_layout.addWidget(self.means_label, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addWidget(self.variance_label, 0, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addWidget(self.std_label, 0, 2, alignment=Qt.AlignmentFlag.AlignLeft)
        self.main_layout.setRowStretch(0, 1)

        self.main_layout.addWidget(self.histogram_label, 10, 0, 1, 10)