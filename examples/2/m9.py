import cv2
import numpy as np

def generate_normal_noise(mean=0, variance=1, image_size=(512, 512)):
    # Generate a random field with normal distribution
    noise_field = np.random.normal(mean, np.sqrt(variance), image_size)

    # Scale the noise to the range [0, 255] for display
    noise_field_scaled = np.clip(noise_field, 0, 255).astype(np.uint8)

    return noise_field_scaled

# Video parameters
mean = 128  # Mean of the normal distribution
variance = 100  # Variance of the normal distribution
image_size = (512, 512)
total_frames = 100  # Number of frames in the video
fps = 30  # Frames per second
output_video_path = 'normal_noise_video.mp4'

# Create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, fps, image_size, isColor=False)

# Simulation
for frame_num in range(total_frames):
    # Generate a new random field for each frame
    noise_frame = generate_normal_noise(mean, variance, image_size)

    # Display the frame
    cv2.imshow("Normal Noise Simulation", noise_frame)

    # Write the frame to the video
    out.write(noise_frame)

    # Adjust the delay as needed for the desired frame rate
    cv2.waitKey(int(1000 / fps))

# Release the VideoWriter
out.release()

print(f"Video saved to {output_video_path}")
