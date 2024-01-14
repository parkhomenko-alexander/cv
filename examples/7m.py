import cv2
import numpy as np
import random

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
image_size = (500, 500)
num_circles = 5
max_radius = 30
speed = 2.0
repulsion_factor = 100.0  # Adjust the repulsion factor as needed
total_frames = 200
fps = 30
output_video_path = 'random_circles_repulsion_video.mp4'

# Create VideoWriter object
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

print(f"Video saved to {output_video_path}")
