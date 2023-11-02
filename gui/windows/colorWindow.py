from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QLabel, QFileDialog, QVBoxLayout, QMenu
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt

import cv2

class ColorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        super().__init__()
        
        color_button = QPushButton("Color", self)
        
        state = {"index": 0, "filters": [cv2.COLOR_BGR2RGB, cv2.COLOR_BGR2HSV, cv2.COLOR_BGR2GRAY]}

        menu = QMenu()
        menu.triggered.connect(lambda x: print(x.text()))

        color_button.setMenu(menu)
        self.add_menu(state["filters"], menu)


    def menu_triggered(self, action):
        print(action.text())

    def add_menu(self, data, menu_obj):
        for index, item in enumerate(data):
            action = menu_obj.addAction(str(index))
            action.setIconVisibleInMenu(False)
            action.setData(index)
