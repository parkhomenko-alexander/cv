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
        
        state = {"RGB": cv2.COLOR_BGR2RGB, "HSV": cv2.COLOR_BGR2HSV, "GRAY": cv2.COLOR_BGR2GRAY}

        menu = QMenu()
        menu.triggered.connect(lambda x: print(x.text()))

        color_button.setMenu(menu)
        self.add_menu(state, menu)


    def menu_triggered(self, action):
        color = action.text()
        if color in self.colors_dict:
            filter_value = self.colors_dict[color]
            print(f"Selected Color: {color}, Filter Value: {filter_value}")

    def add_menu(self, data, menu_obj):
        self.colors_dict = data  # Сохраняем словарь для использования в обработчике
        for color in data.keys():
            action = menu_obj.addAction(color)
            action.setIconVisibleInMenu(False)
