import cv2
import numpy as np

class State:
    # filters = {"RGB": cv2.COLOR_BGR2RGB, "red":"", "HSV": cv2.COLOR_BGR2HSV, "GRAY": cv2.COLOR_BGR2GRAY, }
    filters = ["rgb", "red", "green", "blue", "интенсивность", "яркость"]
    selected_filter = "rgb"

    def filter_image(self, image):
        if self.selected_filter == "red":
            filtered = image.copy()
            filtered[:, :, 1] = 0
            filtered[:, :, 2] = 0
            return filtered
        if self.selected_filter == "green":
            filtered = image.copy()
            filtered[:, :, 0] = 0
            filtered[:, :, 2] = 0
            return filtered
        if self.selected_filter == "blue":
            filtered = image.copy()
            filtered[:, :, 0] = 0
            filtered[:, :, 1] = 0
            return filtered
        if self.selected_filter == "интенсивность":
            filtered = image.copy()
            filtered[:, :, 0] = image[:, :, 0] // 3  
            filtered[:, :, 1] = image[:, :, 1] // 3  
            filtered[:, :, 2] = image[:, :, 2] // 3  
            return filtered
        if self.selected_filter == "яркость":
            return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

state = State()