import cv2
import numpy as np
import random

# Function to generate lattice nodes
def generate_lattice_nodes(K, R, D, orientation, image_size):
    nodes = []
    if orientation == 'straight':
        rows = int(np.sqrt(K))
        cols = int(np.ceil(K / rows))
        for i in range(rows):
            for j in range(cols):
                node_x = int((image_size[1] - 2 * R) * i / (rows - 1) + R)
                node_y = int((image_size[0] - 2 * R) * j / (cols - 1) + R)
                nodes.append({'center': (node_x, node_y), 'radius': R})
    elif orientation == 'oblique':
        cols = int(np.sqrt(K))
        rows = int(np.ceil(K / cols))
        for i in range(rows):
            for j in range(cols):
                node_x = int((image_size[1] - 2 * R) * i / (rows - 1) + R)
                node_y = int((image_size[0] - 2 * R) * j / (cols - 1) + R)
                nodes.append({'center': (node_x, node_y), 'radius': R})
    return nodes

# Function to update circle positions with oscillations
def update_circle_positions_with_oscillations(nodes, amplitude, period, t):
    for node in nodes:
        i0, j0 = node['center']
        fi = random.uniform(0, 2 * np.pi)  # Random oscillation axis
        i_t = i0 + amplitude * np.cos(fi) * np.cos(2 * np.pi * t / period)
        j_t = j0 + amplitude * np.sin(fi) * np.cos(2 * np.pi * t / period)
        node['center'] = (int(i_t), int(j_t))

# Function to draw circles on the image
def draw_circles(image, nodes):
    for node in nodes:
        cv2.circle(image, node['center'], node['radius'], (0, 0, 0), -1)

# Video parameters
image_size = (500, 500)
K = 25  # Number of lattice nodes
R = 20  # Radius of circles
D = 50  # Distance between nodes
orientation = 'oblique'  # 'straight' or 'oblique'
amplitude = 2.0  # Oscillation amplitude
period = 30.0  # Oscillation period
total_frames = 100
fps = 30
output_video_path = 'oscillating_circles_lattice_video.mp4'

# Create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, fps, image_size, isColor=True)

# Generate lattice nodes
nodes = generate_lattice_nodes(K, R, D, orientation, image_size)

# Simulation
for frame_num in range(total_frames):
    t = frame_num / fps  # Time parameter for oscillations
    update_circle_positions_with_oscillations(nodes, amplitude, period, t)

    # Draw circles on the image
    frame = np.ones((image_size[0], image_size[1], 3), dtype=np.uint8) * 255  # White background
    draw_circles(frame, nodes)

    # Write the frame to the video
    out.write(frame)

# Release the VideoWriter
out.release()

print(f"Video saved to {output_video_path}")
