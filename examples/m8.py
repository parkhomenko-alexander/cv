import cv2
import numpy as np

def generate_uniform_noise(a=0, b=1, image_size=(512, 512)):
    noise_field = np.random.uniform(a, b, image_size)
    noise_field_scaled = ((noise_field - a) / (b - a) * 255).astype(np.uint8)
    return noise_field_scaled

# Video parameters
image_size = (512, 512)
total_frames = 100  # Number of frames in the video
fps = 30  # Frames per second
output_video_path = 'uniform_noise_video1.mp4'

# Create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, fps, image_size, isColor=False)

# Simulation
for frame_num in range(total_frames):
    # Dynamically update a and b based on user input or any logic
    a = frame_num / total_frames  # Example: a changes linearly with time
    b = 1

    noise_frame = generate_uniform_noise(a, b, image_size)

    # Write the frame to the video
    out.write(noise_frame)

    # Adjust the delay as needed for the desired frame rate
    cv2.waitKey(int(1000 / fps))

# Release the VideoWriter
out.release()

print(f"Video saved to {output_video_path}")
