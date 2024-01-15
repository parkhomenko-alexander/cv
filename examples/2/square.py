import cv2
import numpy as np

def generate_frame(side_length, frame_size, delta_a, T0, t):
    frame = 255 * np.ones(frame_size, dtype=np.uint8)  # White background

    # Calculate the changing side length
    changing_side = int(side_length + delta_a * np.cos(2 * np.pi * t / T0))

    # Draw a black square with changing side length
    x = (frame_size[0] - changing_side) // 2
    y = (frame_size[1] - changing_side) // 2
    cv2.rectangle(frame, (x, y), (x + changing_side, y + changing_side), 0, thickness=-1)

    return frame

# Set video properties
output_video_path = '../generated_vids/changing_square_video.mp4'
frame_size = (500, 500)
fps = 30
duration_sec = 5

# Set initial side length, delta_a, and T0
side_length = 100
delta_a = 50
T0 = 2

# Create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, fps, frame_size, isColor=False)

# Generate frames and save to video
total_frames = int(fps * duration_sec)
for frame_num in range(total_frames):
    t = frame_num / fps  # Time in seconds
    frame = generate_frame(side_length, frame_size, delta_a, T0, t)

    # Write the frame to the video
    out.write(frame)

# Release the VideoWriter
out.release()

print(f"Video saved to {output_video_path}")
