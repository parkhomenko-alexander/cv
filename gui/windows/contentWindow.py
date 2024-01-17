from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QFileDialog, QGridLayout, QLineEdit, QMenu
from PyQt6.QtGui import QPixmap, QImage, QAction
from PyQt6.QtCore import QTimer, Qt, pyqtSignal

import matplotlib.pyplot as plt

import cv2
import keyboard
import numpy as np
import time
from PIL import ImageGrab
from scipy.stats import skew, kurtosis

from gui.config import config
from gui.windows.analyzeWindow import AnalyzeWindow

from ..state import state

import sys

def plot_combined_histogram(histograms, name, max_size=400):

        def resize_image(image, max_size):
            height, width, _ = image.shape
            aspect_ratio = width / height

            if width > height:
                new_width = max_size
                new_height = int(new_width / aspect_ratio)
            else:
                new_height = max_size
                new_width = int(new_height * aspect_ratio)

            resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
            return resized_image

        plt.figure()

        for h in histograms:
            plt.plot(h["hist"], color=h["color"], label=h["label"])
        
        plt.xlabel('Pixel Value')
        plt.ylabel('Frequency')
        plt.legend()

        # Save the combined histogram as an image with the specified maximum size
        combined_hist_image_path = name
        plt.savefig(combined_hist_image_path, bbox_inches='tight', pad_inches=0, dpi=100)
        plt.clf()  # Clear the figure for the next plot

        combined_hist_image = cv2.imread(combined_hist_image_path)
        combined_hist_image = resize_image(combined_hist_image, max_size)
        plt.close()

        return combined_hist_image

class ContentWindow(QWidget):
    histograms = pyqtSignal(np.ndarray, list, list, list, list, list, list, 
                            list, list, list, list, list, str)

    def __init__(self, fps=config.fps):
        super().__init__()

        # говорит cupture дай мне кадр дай мне кадр очередной
        self.frame_timer = QTimer()
        self.fps = fps
        self.cv_video_capture = cv2.VideoCapture()
        self.is_video_play = False
        self.cv_video_path = None

        # self.filters_state = state

        self.current_image = None
        self.cv_original_image = None
        self.cv_filtered_image = None
        self.is_filter_toggled = False
        # self.prev_image_filter = 


        self.screen_w = config.screen_w
        self.screen_h = config.screen_h


        self.analyze_window = AnalyzeWindow()

        self.analyze_btn = QPushButton("Анализ", self)

        self.menu_bar = menu = QMenu()
        self.statistics_action = QAction("Статистики", self)
        self.statistics = self.menu_bar.addAction(self.statistics_action)
        self.analyze_btn.setMenu(menu)



        self.number_input = QLineEdit(self)
        self.number_input.setPlaceholderText(f"Default fps: {self.fps}")
        self.number_input.setReadOnly(True)


        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("margin-top: 20px;")

        self.image_btn = QPushButton("img")
        self.image_save_btn = QPushButton("save filtered image")
        self.video_btn = QPushButton("video")
        self.play_pause_btn = QPushButton("pause")
        self.filter_btn = QPushButton("filter rgb")
        self.scr_shot_btn = QPushButton("scr_shot")

        self.reset_btn = QPushButton("reset")

        self.main_layout = QGridLayout()


        self.initUI()

        

    def initUI(self):
        # self.modeling_config_window.image_generated.connect(self.display_image)


        self.histograms.connect(self.analyze_window.display_params)


        self.number_input.focusOutEvent = self.focus_out_event
        self.number_input.mouseDoubleClickEvent = self.inputMouseDoubleClickEvent 
        self.number_input.textChanged.connect(self.on_text_changed)

        self.image_btn.clicked.connect(self.load_image)
        self.image_save_btn.clicked.connect(self.save_filtered_image)

        self.video_btn.clicked.connect(self.load_video)
        self.play_pause_btn.clicked.connect(self.play_pause_video)
        self.filter_btn.clicked.connect(self.apply_filter)
        
        self.reset_btn.clicked.connect(self.reset_content)
        self.scr_shot_btn.clicked.connect(self.take_screenshot)

        self.statistics_action.triggered.connect(self.calculate_statistics)

        self.main_layout.addWidget(self.label, 0, 0, 3, 2)
        self.main_layout.addWidget(self.image_btn, 3, 0, 1, 1)
        self.main_layout.addWidget(self.image_save_btn, 3, 1, 1, 1)

        self.main_layout.addWidget(self.video_btn, 4, 0, 1, 1)
        self.main_layout.addWidget(self.play_pause_btn, 4, 1, 1, 1)

        self.main_layout.addWidget(self.filter_btn, 5, 0, 1, 2)

        self.main_layout.addWidget(self.reset_btn, 6, 0, 1, 2)
        self.main_layout.addWidget(self.scr_shot_btn, 7, 0, 1, 2)
        self.main_layout.addWidget(self.number_input, 8, 0, 1, 2)


        self.setLayout(self.main_layout)

        self.setWindowTitle('Content')
        self.setGeometry(200, 200, self.screen_w, self.screen_h)


    #* IMAGES ==============================
    def load_image(self, image):
        if  image is not False: 
            self.cv_original_image = image
            self.display_image(self.cv_original_image)
            return 
        
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
                self.current_image = cv2.cvtColor(self.cv_original_image, cv2.COLOR_BGR2GRAY)
                if image is not None:
                    # v rgb
                    height, width, channel = image.shape
                    scale_factor = 1
                    new_w = 400
                    new_h = int(new_w * height / width) 
                    resized_img = self.resize_image(new_w, new_h)
                    self.cv_original_image = resized_img
                    if self.is_filter_toggled:
                        self.cv_filtered_image = state.filter_image(self.cv_original_image)
                        self.display_image(self.cv_filtered_image)
                    else:
                        self.display_image(self.cv_original_image)
    
    def display_image(self, img_for_display):
        if img_for_display is not None:
            q_image = self.convert_cv_to_qimage(img_for_display)
            self.label.setPixmap(QPixmap.fromImage(q_image))
    

    def convert_cv_to_qimage(self, cv_image):
        height, width, *channel = cv_image.shape
        if self.is_filter_toggled and state.selected_filter=="яркость":
            bytes_per_line = 1 * width
            return QImage(cv_image.data, width, height, bytes_per_line, QImage.Format.Format_Grayscale8)
        else:
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

    def take_screenshot(self):
        keyboard.send('shift+windows+s')
        time.sleep(3)
        clipboard_image = ImageGrab.grabclipboard()
        if clipboard_image:
            clipboard_array = np.array(clipboard_image)
            clipboard_rgb = cv2.cvtColor(clipboard_array, cv2.COLOR_RGBA2RGB)
            self.cv_original_image = clipboard_rgb
            self.display_image(self.cv_original_image)
        else:
            print('No image found on the clipboard')
    #* IMAGES END ==============================
    

    #* VEDIO ==============================
    def play_pause_video(self):
        if not self.cv_video_capture.isOpened():
            return
        if self.is_video_play is False:
            self.play_pause_btn.setText('pause')
            self.frame_timer.timeout.connect(self.display_video)
            self.frame_timer.start(int(1000//self.fps))

            ret, frame = self.cv_video_capture.read()
            self.current_image = frame
            self.cv_filtered_image = state.filter_image(frame)
            if state.selected_filter == "яркость":
                self.current_image = frame
            else:
                self.current_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        else:
            self.frame_timer.timeout.disconnect(self.display_video)
            self.frame_timer.stop()
            self.play_pause_btn.setText('play')
        self.is_video_play = not self.is_video_play
    
    def load_video(self, path):
        self.reset_content()
        if path is not False:
            self.cv_video_path = sys.path[1] + "/" + path
            self.cv_video_capture.open(self.cv_video_path)
            self.play_pause_video()
            return 
        
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
                    frame = state.filter_image(frame)
                else:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


                if self.is_filter_toggled and state.selected_filter=="яркость":
                    h, w, *ch = frame.shape
                    qt_image = QImage(frame.data, w, h, w, QImage.Format.Format_Grayscale8)
                else:
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
        # 0 0 1
        # 1 1 1
        # 0 1 0
        # 1 0 0
        if state.selected_filter == "rgb":
            return 
        if self.cv_video_capture is None and self.cv_original_image is None:
            print('исходники не загружены')
            return

        if not self.is_filter_toggled:
            self.is_filter_toggled = True
            
            if self.cv_original_image is not None:
                self.cv_filtered_image = state.filter_image(self.cv_original_image)
                self.display_image(self.cv_filtered_image)
            self.filter_btn.setText("filter " + state.selected_filter)
            if state.selected_filter == "яркость":
                self.current_image = self.cv_filtered_image
            else:
                self.current_image = cv2.cvtColor(self.cv_filtered_image, cv2.COLOR_BGR2GRAY)


        else:
            self.is_filter_toggled = False

            if self.cv_original_image is not None:
                self.display_image(self.cv_original_image)
            self.filter_btn.setText("filter rgb")
    #* FILTERS END ==============================


    #* ANALYZE ==============================
    def calculate_histograms(self, image):
        histograms = []

        if True:
            histograms = [
                {
                    "hist": cv2.calcHist([image], [0], None, [256], [0, 256]),
                    "color": 'black', 
                    "label":'Grayscale'
                }
            ]
            hist = plot_combined_histogram(histograms, "generated_img/hist.png")
            return hist
            
        b, g, r = cv2.split(image)

        name = "generated_img/hist.png"
        hist_b = cv2.calcHist([b], [0], None, [256], [0, 256])
        hist_g = cv2.calcHist([g], [0], None, [256], [0, 256])
        hist_r = cv2.calcHist([r], [0], None, [256], [0, 256])
        histograms = [
            {
                "hist": hist_b,
                "color": 'blue', 
                "label":'Blue Channel'
            },
            {
                "hist": hist_g,
                "color": 'green', 
                "label":'Green Channel'
            },
            {
                "hist": hist_r,
                "color": 'red', 
                "label":'Red Channel'
            }
        ]

        hist = plot_combined_histogram(histograms, "generated_img/hist.png")

        return hist 
    
    def calculate_means(self, image):

        if True:
            means = [
                {
                    "val": round(cv2.mean(image)[0],2),
                    "name": "GS"
                }
            ]
            return means

        b, g, r = cv2.split(image)
        means = [
            {
                "val": int(np.mean(b)),
                "name": "B"
            },
            {
                "val": int(np.mean(g)),
                "name": "G"
            }, {
                "val": int(np.mean(r)),
                "name": "R"
            }
        ]

        return means
    
    def calculate_dispersion(self, image):

        if True:
            variance = [
                {
                    "val": round(np.var(image),2),
                    "name": "GS"
                }
            ]
            return variance
        
        b, g, r = cv2.split(image)
        variance = [
            {
                "val": int(np.var(b)),
                "name": "B"
            },
            {
                "val": int(np.var(g)),
                "name": "G"
            }, {
                "val": int(np.var(r)),
                "name": "R"
            }
        ]

        return variance
    
    def calculate_std(self, image):

        if True:
            vals = [
                {
                    "val": round(np.std(image),2),
                    "name": "GS"
                }
            ]
            return vals 
        
        b, g, r = cv2.split(image)
        vals = [
            {
                "val": int(np.std(b)),
                "name": "B"
            },
            {
                "val": int(np.std(g)),
                "name": "G"
            }, {
                "val": int(np.std(r)),
                "name": "R"
            }
        ]

        return vals
    
    def calculate_skew(self, image):

        if True:
            vals = [
                {
                    "val": round(skew(image.flatten()),2),
                    "name": "GS"
                }
            ]
            return vals 
        
        b, g, r = cv2.split(image)
        vals = [
            {
                "val": int(skew(b.flatten())),
                "name": "B"
            },
            {
                "val": int(skew(g.flatten())),
                "name": "G"
            }, {
                "val": int(skew(r.flatten())),
                "name": "R"
            }
        ]

        return vals
    
    def calculate_kurtosis(self, image):

        if True:
            vals = [
                {
                    "val": round(kurtosis(image.flatten()),2),
                    "name": "GS"
                }
            ]
            return vals 
    
        b, g, r = cv2.split(image)
        vals = [
            {
                "val": int(kurtosis(b.flatten(), fisher=True)),
                "name": "B"
            },
            {
                "val": int(kurtosis(g.flatten(), fisher=True)),
                "name": "G"
            }, {
                "val": int(kurtosis(r.flatten(), fisher=True)),
                "name": "R"
            }
        ]

        return vals
    
    def calculate_variance(self, image):

        if True:
            mean_value = np.mean(image)
            std_deviation = np.std(image)
            vals = [
                {
                    "val": round((std_deviation / mean_value) * 100, 2),
                    "name": "GS"
                }
            ]
            return vals 
        
        b, g, r = cv2.split(image)
        mean_b, mean_g, mean_r = np.mean(b), np.mean(g), np.mean(r)
        std_dev_b, std_dev_g, std_dev_r = np.std(b), np.std(g), np.std(r)

        cv_b = (std_dev_b / mean_b) * 100
        cv_g = (std_dev_g / mean_g) * 100
        cv_r = (std_dev_r / mean_r) * 100

        vals = [
            {
                "val": int(cv_b),
                "name": "B"
            },
            {
                "val": int(cv_g),
                "name": "G"
            }, {
                "val": int(cv_r),
                "name": "R"
            }
        ]

        return vals
    
    def calculate_min(self, image):

        if True:
            vals = [
                {
                    "val": round(np.min(image), 2),
                    "name": "GS"
                }
            ]
            return vals 

        b, g, r = cv2.split(image)
        vals = [
            {
                "val": np.min(b),
                "name": "B"
            },
            {
                "val": np.min(g),
                "name": "G"
            }, {
                "val": np.min(r),
                "name": "R"
            }
        ]

        return vals
    
    def calculate_max(self, image):

        if True:
            vals = [
                {
                    "val": round(np.max(image), 2),
                    "name": "GS"
                }
            ]
            return vals 

        b, g, r = cv2.split(image)
        vals = [
            {
                "val": np.max(b),
                "name": "B"
            },
            {
                "val": np.max(g),
                "name": "G"
            }, {
                "val": np.max(r),
                "name": "R"
            }
        ]

        return vals
    
    def calculate_percentile5(self, image):

        if True:
            vals = [
                {
                    "val": round(np.percentile(image, 5), 2),
                    "name": "GS"
                }
            ]
            return vals 

        b, g, r = cv2.split(image)
        vals = [
            {
                "val": np.percentile(b.flatten(), 5),
                "name": "B"
            },
            {
                "val": np.percentile(g.flatten(), 5),
                "name": "G"
            }, {
                "val": np.percentile(r.flatten(), 5),
                "name": "R"
            }
        ]

        return vals
    
    def calculate_percentile95(self, image):

        if True:
            vals = [
                {
                    "val": round(np.percentile(image, 95), 2),
                    "name": "GS"
                }
            ]
            return vals 

        b, g, r = cv2.split(image)
        vals = [
            {
                "val": np.percentile(b.flatten(), 95),
                "name": "B"
            },
            {
                "val": np.percentile(g.flatten(), 95),
                "name": "G"
            }, {
                "val": np.percentile(r.flatten(), 95),
                "name": "R"
            }
        ]

        return vals
    
    def calculate_median(self, image):

        if True:
            vals = [
                {
                    "val": round(np.median(image), 2),
                    "name": "GS"
                }
            ]
            return vals 

        b, g, r = cv2.split(image)
        vals = [
            {
                "val": np.median(b),
                "name": "B"
            },
            {
                "val": np.median(g),
                "name": "G"
            }, {
                "val": np.median(r),
                "name": "R"
            }
        ]

        return vals


    def calculate_statistics(self):
        # hist = self.calculate_histograms(self.cv_original_image)
        hist = self.calculate_histograms(self.current_image)
        means = self.calculate_means(self.current_image)
        varsiance = self.calculate_dispersion(self.current_image)
        std = self.calculate_std(self.current_image)
        skew = self.calculate_skew(self.current_image)
        kurtosis = self.calculate_kurtosis(self.current_image)
        variance = self.calculate_variance(self.current_image)
        mins = self.calculate_min(self.current_image)
        maxs = self.calculate_max(self.current_image)
        percentil5 = self.calculate_percentile5(self.current_image)
        percentil95 = self.calculate_percentile95(self.current_image)
        median = self.calculate_median(self.current_image)

        self.histograms.emit(hist, means, varsiance, std, skew, kurtosis,
                             variance, mins, maxs, percentil5, percentil95,
                             median, "generated_img/hist.png")

        self.analyze_window.show()
        print("analyze") 
    #* ANALYZE END ==============================


    def inputMouseDoubleClickEvent(self, event):
        print('zxczczxczx')
        self.number_input.setReadOnly(False) 
            
    def focus_out_event(self, event):
        self.number_input.setReadOnly(True)

    def on_text_changed(self, text):
        try:
            self.fps = int(text)  # Convert the input text to a number
            self.frame_timer.start(int(1000//self.fps))
        except ValueError:
            self.number = None  # Reset the variable if it's not a valid number

    def reset_content(self):
        self.cv_original_image = None
        if self.frame_timer.isActive():
            self.frame_timer.stop()
        self.cv_video_capture.release()
        self.cv_video_capture = cv2.VideoCapture()
        self.label.setPixmap(QPixmap())
        self.cv_original_image = None