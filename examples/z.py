import cv2
import numpy as np
import os

# Function to generate a frame with a changing radius circle
def generate_frame(radius, center, frame_size, deltaR, T0, t):
    frame = 255 * np.ones(frame_size, dtype=np.uint8)  # White background

    # Calculate the changing radius
    changing_radius = int(radius + deltaR * np.cos(2 * np.pi * t / T0))

    # Draw a black circle with changing radius
    cv2.circle(frame, center, changing_radius, 0, thickness=-1)

    return frame

# Set the output video file path
output_video_path = "generated_vids/changing_radius_circle_video.avi"

# Set the input frames directory
input_frames_directory = "changing_radius_frames"

# Set the initial radius, deltaR, and T0
radius = 50
deltaR = 30
T0 = 2

# Set the total number of frames and frame duration
total_frames = 150
fps = 30

# Create VideoWriter object
frame_size = (500, 500)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(output_video_path, fourcc, fps, frame_size, isColor=False)

# Generate frames and save to video
for frame_num in range(total_frames):
    t = frame_num / fps  # Time in seconds
    frame = generate_frame(radius, (250, 250), frame_size, deltaR, T0, t)

    # Write the frame to the video
    out.write(frame)

# Release the VideoWriter
out.release()

print(f"Video saved to {output_video_path}")
