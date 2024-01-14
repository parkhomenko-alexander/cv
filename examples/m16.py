import cv2
import numpy as np

def generate_chessboard_nodes(K, R, D, orientation, image_size):
    nodes = []
    rows = int(np.sqrt(K))
    cols = int(np.ceil(K / rows))
    for i in range(rows):
        for j in range(cols):
            if (i + j) % 2 == 0:
                node_x = int((image_size[1] - 2 * R) * i / (rows - 1) + R)
                node_y = int((image_size[0] - 2 * R) * j / (cols - 1) + R)
                nodes.append({'center': (node_x, node_y), 'radius': R})
    return nodes

# Function to draw circles on the image
def draw_circles(image, nodes):
    for node in nodes:
        cv2.circle(image, node['center'], node['radius'], (0, 0, 0), -1)

# Video parameters
image_size = (500, 500)
K = 25  # Number of lattice nodes
R = 20  # Radius of circles
D = 50  # Distance between nodes
orientation = 'straight'  # 'straight' or 'oblique'
total_frames = 1  # A single frame for a static image
fps = 30
output_image_path = 'chessboard_circles_image.png'

# Create a blank image
image = np.ones((image_size[0], image_size[1], 3), dtype=np.uint8) * 255  # White background

# Generate chessboard nodes
nodes = generate_chessboard_nodes(K, R, D, orientation, image_size)

# Draw circles on the image
draw_circles(image, nodes)

# Save the image
cv2.imwrite(output_image_path, image)

print(f"Image saved to {output_image_path}")
