from PyQt6.QtWidgets import QWidget, QPushButton, QMenu
from PyQt6.QtGui import QAction

# from ..state import state, selected_filter
from ..state import state

class ColorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        super().__init__()
        
        self.color_button = QPushButton(state.selected_filter, self)
        
        menu = QMenu()
        # menu.triggered.connect(lambda x: print(x.text()))
        color_schemes = state.filters

        for scheme in color_schemes:
            action = QAction(scheme, self)
            action.triggered.connect(self.update_color_scheme)
            menu.addAction(action)
        self.color_button.setMenu(menu)
        # self.add_menu(state, menu)

    def update_color_scheme(self):
        action = self.sender()  # Get the triggered QAction
        if action:
            self.color_scheme = action.text()
            state.selected_filter = action.text()
            print(state.selected_filter)
            self.color_button.setText(state.selected_filter)

    # def menu_triggered(self, action):
    #     color = action.text()
    #     if color in self.colors_dict:
    #         filter_value = self.colors_dict[color]
    #         print(f"Selected Color: {color}, Filter Value: {filter_value}")

    # def add_menu(self, data, menu_obj):
    #     self.colors_dict = data  # Сохраняем словарь для использования в обработчике
    #     for color in data.keys():
    #         action = menu_obj.addAction(color)
    #         action.setIconVisibleInMenu(False)
