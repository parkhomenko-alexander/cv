from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QFileDialog, QGridLayout
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import QTimer, Qt

import cv2
import numpy as np

class ContentWindow(QWidget):
    def __init__(self, fps=20):
        super().__init__()

        # говорит cupture дай мне кадр дай мне кадр очередной
        self.frame_timer = QTimer()
        self.fps = fps
        self.cv_video_capture = cv2.VideoCapture()
        self.is_video_play = False
        self.cv_video_path = None

        self.cv_original_image = None
        self.cv_filtered_image = None
        self.is_filter_toggled = False
        # self.prev_image_filter = 


        self.screen_w = 400
        self.screen_h = 400

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.image_btn = QPushButton("img")
        self.image_save_btn = QPushButton("save filtered image")
        self.video_btn = QPushButton("video")
        self.play_pause_btn = QPushButton("pause")
        self.filter_btn = QPushButton("aplly filter")

        self.reset_btn = QPushButton("reset")

        self.main_layout = QGridLayout()

        self.initUI()

        

    def initUI(self):
        self.image_btn.clicked.connect(self.load_image)
        self.image_save_btn.clicked.connect(self.save_filtered_image)

        self.video_btn.clicked.connect(self.load_video)
        self.play_pause_btn.clicked.connect(self.play_pause_video)
        self.filter_btn.clicked.connect(self.apply_filter)
        
        self.reset_btn.clicked.connect(self.reset_content) 

        self.main_layout.addWidget(self.label, 0, 0, 3, 2)
        self.main_layout.addWidget(self.image_btn, 3, 0, 1, 1)
        self.main_layout.addWidget(self.image_save_btn, 3, 1, 1, 1)

        self.main_layout.addWidget(self.video_btn, 4, 0, 1, 1)
        self.main_layout.addWidget(self.play_pause_btn, 4, 1, 1, 1)

        self.main_layout.addWidget(self.filter_btn, 5, 0, 1, 2)

        self.main_layout.addWidget(self.reset_btn, 6, 0, 1, 2)
        

        self.setLayout(self.main_layout)

        self.setWindowTitle('Content')
        self.setGeometry(200, 200, self.screen_w, self.screen_h)

    # def resizeEvent(self, event):
    #     width = event.size().width()
    #     height = event.size().height()
        
    #     # if (abs(width - self.screen_w)) != (abs(height - self.screen_h)):
    #     #     return 

    #     w_aspect = width / self.screen_w
    #     h_aspect = height / self.screen_h

    #     self.screen_w = width
    #     self.screen_h = height

    #     if self.cv_original_image is not None:
    #         h, w,  *rest = self.cv_original_image.shape
    #         self.resize_image(int(w*w_aspect), int(h*h_aspect))

    #         self.display_image()


    #* IMAGES ==============================
    def load_image(self):
        self.cv_video_capture = cv2.VideoCapture()
        if self.frame_timer.isActive():
            self.frame_timer.stop()

        dialog = QFileDialog(self)
        dialog.setDirectory(r'C:\images')
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Images (*.png *.jpg)")
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filenames = dialog.selectedFiles()
            if filenames:
                image = cv2.imread(filenames[0])
                self.cv_original_image = image
                if image is not None:
                    # v rgb
                    height, width, channel = image.shape
                    scale_factor = 1
                    new_w = 400
                    new_h = int(new_w * height / width) 
                    # print(new_w, new_h, channel)
                    resized_img = self.resize_image(new_w, new_h)
                    self.cv_original_image = resized_img
                    self.display_image(self.cv_original_image)

    def display_image(self, img_for_display):
        if img_for_display is not None:
            q_image = self.convert_cv_to_qimage(img_for_display)
            self.label.setPixmap(QPixmap.fromImage(q_image))
            # self.label.setScaledContents(True)

    def convert_cv_to_qimage(self, cv_image):
        height, width, channel = cv_image.shape
        bytes_per_line = 3 * width
        return QImage(cv_image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)

    def resize_image(self, new_w, new_h,):
        self.cv_original_image = cv2.resize(self.cv_original_image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
        self.cv_original_image = cv2.cvtColor(self.cv_original_image, cv2.COLOR_BGR2RGB)
        return self.cv_original_image
    
    def save_filtered_image(self,):
        if self.cv_filtered_image is not None:
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getSaveFileName(self, 'Save Image', '', 'Images (*.png *.jpg *.jpeg *.bmp);;All Files (*)')
            if file_path:
                cv2.imwrite(file_path, self.cv_filtered_image)
                print(f"Image saved to {file_path}")
        else:
            print('нет изображения с фильтром')

    #* IMAGES END ==============================
    

    #* VEDIO ==============================
    def play_pause_video(self):
        if not self.cv_video_capture.isOpened():
            return
        if self.is_video_play is False:
            self.play_pause_btn.setText('pause')
            self.frame_timer.timeout.connect(self.display_video)
            self.frame_timer.start(int(1000//self.fps))
            self.is_video_play = True
        else:
            self.frame_timer.stop()
            self.play_pause_btn.setText('play')
            self.is_video_play = False
    
    def load_video(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setDirectory(r'C:\images')
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Video Files (*.mp4 *.avi *.mkv);;All Files (*)")

        if dialog.exec():
            self.cv_video_path = dialog.selectedFiles()[0]
            self.cv_video_capture.open(self.cv_video_path)
            self.play_pause_video()

    def display_video(self):
            ret, frame = self.cv_video_capture.read()

            if ret:
                # Конвертируем кадр в формат QImage
                if self.is_filter_toggled: 
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                else:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


                h, w, ch = frame.shape
                bytes_per_line = ch * w
                qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)

                # Отображаем кадр в QLabel
                pixmap = QPixmap.fromImage(qt_image)
                self.label.setPixmap(pixmap)
            else:
                self.cv_video_capture.release()
                self.cv_video_capture.open(self.cv_video_path)
    #* VIDEO END ==============================


    #* FILTERS ==============================
    def apply_filter(self):
        if self.cv_original_image is None:
            print('изображение не загружено')
            return

        if not self.is_filter_toggled:
            self.is_filter_toggled = True
            self.cv_filtered_image = cv2.GaussianBlur(self.cv_original_image, (15, 15), 0)
            self.display_image(self.cv_filtered_image)
        else:
            self.is_filter_toggled = False
            self.display_image(self.cv_original_image)
    #* FILTERS END ==============================


    def reset_content(self):
        self.cv_original_image = None
        if self.frame_timer.isActive():
            self.frame_timer.stop()
        self.cv_video_capture.release()
        self.cv_video_capture = cv2.VideoCapture()
        self.label.setPixmap(QPixmap())
