
from PyQt6.QtWidgets import QWidget, QPushButton, QLineEdit, QGridLayout
from PyQt6.QtCore import pyqtSignal


import cv2
import numpy as np

from gui.windows.contentWindow import config
import random
# from gui.windows.contentWindow import ContentWindow 

class ModelingConfigWindow(QWidget):
    image_generated = pyqtSignal(np.ndarray)
    video_generate = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        # self.image_generated = np.ndarray

        self.width, self.height = config.screen_w, config.screen_h 

        self.input_model = QLineEdit(self)
        self.input_model.setPlaceholderText(f"Model")

        
        self.model_1 = QPushButton("Задержанный единичный импульс")
        self.model_2 = QPushButton("Задержанный единичный скачок")
        self.model_3 = QPushButton("Одиночный круг радиуса R")
        self.model_4 = QPushButton("Одиночный квадрат со стороной a")
        self.model_5 = QPushButton("Шахматная доска")
        self.model_6 = QPushButton("Круги в узлах прямоугольной решетки")
        self.model_7 = QPushButton("Случайные  круги")
        self.model_8 = QPushButton("Белый шум с равномерным распределением")
        self.model_9 = QPushButton("Белый шум с нормальным распределением")
        self.model_10 = QPushButton("Плоская гравитационная волна")

        self.main_layout = QGridLayout()

        # self.content_window = ContentWindow
        self.setWindowTitle('Describe model')

        self.initUI()

    def initUI(self):
        super().__init__()

        self.model_1.clicked.connect(self.generate_model_1)  
        self.model_2.clicked.connect(self.generate_model_2)  
        self.model_3.clicked.connect(self.generate_model_3)  
        self.model_4.clicked.connect(self.generate_model_4)  
        self.model_5.clicked.connect(self.generate_model_5)  
        self.model_7.clicked.connect(self.generate_model_7)  
        self.model_8.clicked.connect(self.generate_model_8)  
        self.model_9.clicked.connect(self.generate_model_9)  


        self.main_layout.addWidget(self.input_model, 0, 0, 1, 1)
        
        self.main_layout.addWidget(self.model_1, 1, 0, 1, 1)
        self.main_layout.addWidget(self.model_2, 2, 0, 1, 1)
        self.main_layout.addWidget(self.model_3, 3, 0, 1, 1)
        self.main_layout.addWidget(self.model_4, 4, 0, 1, 1)
        self.main_layout.addWidget(self.model_5, 5, 0, 1, 1)
        self.main_layout.addWidget(self.model_6, 6, 0, 1, 1)
        self.main_layout.addWidget(self.model_7, 7, 0, 1, 1)
        self.main_layout.addWidget(self.model_8, 8, 0, 1, 1)
        self.main_layout.addWidget(self.model_9, 9, 0, 1, 1)
        self.main_layout.addWidget(self.model_10, 10, 0, 1, 1)

        
        self.setLayout(self.main_layout)
    
    def parse_params(self):
        params = self.input_model.text().split(" ")
        return params
    
    def generate_model_1(self):
        params = self.parse_params()

        img = np.ones((self.height, self.width, 3), dtype=np.uint8) * 255

        rectangle_height = 20
        rectangle_width = 3
        i0 = int(params[0]) # x
        j0 = int(params[1]) # y
        top_left = (i0, self.height - (j0 + rectangle_height))
        bottom_right = (i0 + rectangle_width, self.height - j0)
        rec = cv2.rectangle(img, top_left, bottom_right, 0, thickness=cv2.FILLED)
        print(top_left, bottom_right, type(rec))
        self.image_generated.emit(img)

    def generate_model_2(self):
        params = self.parse_params()

        img = np.ones((self.height, self.width, 3), dtype=np.uint8) * 255

        i0 = int(params[0]) # x
        j0 = int(params[1]) # y
        top_left = (i0, self.height - j0)
        bottom_right = (self.width, 0)
        rec = cv2.rectangle(img, top_left, bottom_right, 0, thickness=cv2.FILLED)
        self.image_generated.emit(img)

    def generate_model_3(self):
        def generate_frame(radius, center, frame_size, deltaR, T0, t):
            frame = 255 * np.ones(frame_size, dtype=np.uint8)  
            changing_radius = int(radius + deltaR * np.cos(2 * np.pi * t / T0))
            cv2.circle(frame, center, changing_radius, 0, thickness=-1)

            return frame
        
        output_video_path  = 'generated_vids/changing_radius_circle_formula.mp4'
        frame_size = (self.height, self.width)
        fps = config.fps
        duration_sec = 5
        center = (frame_size[0] // 2, frame_size[1] // 2)

        params = self.parse_params()

        radius = 50
        deltaR = int(params[0])
        T0 = int(params[1])

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_video_path, fourcc, fps, frame_size, isColor=False)
        total_frames = int(fps * duration_sec)
        for frame_num in range(total_frames):
            t = frame_num / fps 
            frame = generate_frame(radius, center, frame_size, deltaR, T0, t)
            out.write(frame)

        out.release()
        self.video_generate.emit(output_video_path)

    def generate_model_4(self):
        def generate_frame(side_length, frame_size, deltaR, T0, t):
            frame = 255 * np.ones(frame_size, dtype=np.uint8)  
            changing_side = int(side_length + deltaR * np.cos(2 * np.pi * t / T0))
            x = (frame_size[0] - changing_side) // 2
            y = (frame_size[1] - changing_side) // 2
            cv2.rectangle(frame, (x, y), (x + changing_side, y + changing_side), 0, thickness=-1)

            return frame
        
        output_video_path  = 'generated_vids/changing_radius_circle_formula.mp4'
        frame_size = (self.height, self.width)
        fps = config.fps
        duration_sec = 5

        params = self.parse_params()

        side_length = 100
        delta_a = int(params[0])
        T0 = int(params[1])

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_video_path, fourcc, fps, frame_size, isColor=False)
        total_frames = int(fps * duration_sec)
        for frame_num in range(total_frames):
            t = frame_num / fps  
            frame = generate_frame(side_length, frame_size, delta_a, T0, t)
            out.write(frame)

        out.release()
        self.video_generate.emit(output_video_path)
        
    def generate_model_5(self):
        params = self.parse_params()
        p1 = int(params[0])
        p2 = int(params[1])

        total_size = p1 * p2

        # Create a white background
        chessboard = np.ones((total_size, total_size, 3), dtype=np.uint8) * 255

        for i in range(p1):
            for j in range(p1):
                # Calculate the starting point of each cell
                x = j * p2
                y = i * p2

                # Draw a black or white square based on the cell indices
                if (i + j) % 2 == 0:
                    cv2.rectangle(chessboard, (x, y), (x + p2, y + p2), 0, thickness=-1)

        self.image_generated.emit(chessboard)
    
    def generate_model_7(self):
        def generate_random_circles(num_circles, max_radius, image_size):
            circles = []
            for _ in range(num_circles):
                radius = random.randint(5, max_radius)
                center = (random.randint(radius, image_size[1] - radius), random.randint(radius, image_size[0] - radius))
                direction = random.uniform(0, 2 * np.pi)
                circles.append({'center': center, 'radius': radius, 'direction': direction})
            return circles

        def update_circle_positions(circles, speed, repulsion_factor, image_size):
            for i in range(len(circles)):
                x, y = circles[i]['center']
                direction = circles[i]['direction']

                # Update circle position based on linear movement
                x += speed * np.cos(direction)
                y += speed * np.sin(direction)

                # Repulsion from other circles
                for j in range(len(circles)):
                    if i != j:
                        distance = np.sqrt((x - circles[j]['center'][0]) ** 2 + (y - circles[j]['center'][1]) ** 2)
                        if distance < circles[i]['radius'] + circles[j]['radius']:
                            # Apply repulsion force
                            repulsion_force = repulsion_factor / distance
                            direction += repulsion_force * np.arctan2(y - circles[j]['center'][1], x - circles[j]['center'][0])

                # Check and reflect at boundaries
                if x - circles[i]['radius'] < 0 or x + circles[i]['radius'] >= image_size[1]:
                    direction = np.pi - direction
                if y - circles[i]['radius'] < 0 or y + circles[i]['radius'] >= image_size[0]:
                    direction = -direction

                circles[i]['center'] = (x, y)
                circles[i]['direction'] = direction

        def draw_circles(image, circles):
            for circle in circles:
                cv2.circle(image, (int(circle['center'][0]), int(circle['center'][1])), circle['radius'], (0, 0, 0), -1)

        # Video parameters
        image_size = (self.width, self.height)
        num_circles = 5
        max_radius = 30
        speed = 2.0
        repulsion_factor = 100.0  # Adjust the repulsion factor as needed
        total_frames = 200
        fps = 30
        output_video_path = 'generated_vids/random_circles_repulsion_video.mp4'

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_video_path, fourcc, fps, image_size, isColor=True)

        # Generate random circles
        circles = generate_random_circles(num_circles, max_radius, image_size)

        # Simulation
        for frame_num in range(total_frames):
            # Update circle positions with repulsion
            update_circle_positions(circles, speed, repulsion_factor, image_size)

            # Draw circles on the image
            frame = np.ones((image_size[0], image_size[1], 3), dtype=np.uint8) * 255  # White background
            draw_circles(frame, circles)

            # Write the frame to the video
            out.write(frame)

        # Release the VideoWriter
        out.release()
        self.video_generate.emit(output_video_path)

    
    def generate_model_8(self):
        params = self.parse_params()
        p1 = 0
        p2 = 1 
        if params[0] != "":
            p1 = int(params[0])
            p2 = int(params[1])
        print(p1, p2)

        image_size = (self.height, self.width)

        def generate_uniform_noise(a=0, b=1, image_size=image_size):
            noise_field = np.random.uniform(a, b, image_size)
            noise_field_scaled = ((noise_field - a) / (b - a) * 255).astype(np.uint8)
            return noise_field_scaled

        total_frames = 100  
        fps = 30  
        output_video_path = 'generated_vids/uniform_noise_video.mp4'

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_video_path, fourcc, fps, image_size, isColor=False)

        for frame_num in range(total_frames):
            noise_frame = generate_uniform_noise(p1, p2, image_size)
            out.write(noise_frame)

        out.release()
        self.video_generate.emit(output_video_path)

    def generate_model_9(self):
        image_size = (self.height, self.width)

        def generate_normal_noise(mean=0, variance=1, image_size=(512, 512)):
            noise_field = np.random.normal(mean, np.sqrt(variance), image_size)
            noise_field_scaled = np.clip(noise_field, 0, 255).astype(np.uint8)

            return noise_field_scaled
        
        mean = 128  # Mean of the normal distribution
        variance = 100  # Variance of the normal distribution
        total_frames = 100  # Number of frames in the video
        fps = 30  # Frames per second
        output_video_path = 'generated_vids/normal_noise_video.mp4'

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_video_path, fourcc, fps, image_size, isColor=False)

        for frame_num in range(total_frames):
            noise_frame = generate_normal_noise(mean, variance, image_size)
            out.write(noise_frame)

        out.release()
        self.video_generate.emit(output_video_path)
