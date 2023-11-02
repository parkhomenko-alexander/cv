from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QLabel, QFileDialog, QVBoxLayout
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt

import cv2

class ContentWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        button_layout = QHBoxLayout()

        image_button = QPushButton("img", self)
        # image_button.setToolTip("Open file")
        image_button.clicked.connect(self.open_image)

        video_button = QPushButton("video", self)
        video_button.clicked.connect(self.open_video)

        button_layout.addWidget(image_button)
        button_layout.addWidget(video_button)

        button_widget = QWidget()
        button_widget.setLayout(button_layout)

        button_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 20)
        main_layout.addWidget(button_widget)  # Add the button
        main_layout.addWidget(self.label)  # Add the label for the image
        # main_layout.addWidget(self.video_widget)  # Add the label for the image

        # Set the main layout for the widget
        self.setLayout(main_layout)

        self.setWindowTitle('Content')
        self.setGeometry(200, 200, 200, 200)

        



    def open_image(self):
        dialog = QFileDialog(self)
        dialog.setDirectory(r'C:\images')
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Images (*.png *.jpg)")
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filenames = dialog.selectedFiles()
            if filenames:
                # Load the first selected image and display it
                pixmap = QPixmap(filenames[0])
                # self.label.setPixmap(pixmap)
                # self.label.setScaledContents(True)
                self.label.setPixmap(pixmap)

                self.label.adjustSize()
                self.setWindowTitle(filenames[0])

    def open_video(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)

        if dialog.exec():
            filename = dialog.selectedFiles()[0]

            cap = cv2.VideoCapture(filename)
            while cap.isOpened():
                ret, frame = cap.read()

                if ret:
                    # Конвертируем кадр в формат QImage
                    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    h, w, ch = rgb_image.shape
                    bytes_per_line = ch * w
                    qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)

                    # Отображаем кадр в QLabel
                    pixmap = QPixmap.fromImage(qt_image)
                    self.label.setPixmap(pixmap)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()
        
