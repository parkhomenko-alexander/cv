import numpy as np
import cv2

# Parameters
amplitude = 50.0  # Amplitude of the wave
period = 10.0  # Period of the wave (time for one complete oscillation)
wave_speed = 1.0  # Wave speed (related to gravitational acceleration)

# Function to generate a flat gravity wave
def generate_gravity_wave(time, amplitude, period, wave_speed, spatial_points):
    wavelength = wave_speed * period  # Relationship between wave speed, period, and wavelength
    wave_function = amplitude * np.sin(2 * np.pi / wavelength * (wave_speed * time - spatial_points))
    return wave_function

# Video parameters
spatial_points = np.linspace(0, 100, 500)  # Spatial points along the x-axis
total_frames = 100  # Number of frames in the video
fps = 30  # Frames per second
output_video_path = 'gravity_wave_video.mp4'

# Create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, fps, (500, 500))

# Generate video frames
for frame_num in range(total_frames):
    time = frame_num / fps  # Time parameter (adjust as needed)
    wave_frame = generate_gravity_wave(time, amplitude, period, wave_speed, spatial_points)

    # Normalize values to the range [0, 255] for display
    normalized_wave_frame = ((wave_frame - np.min(wave_frame)) / (np.max(wave_frame) - np.min(wave_frame)) * 255).astype(np.uint8)

    # Convert to 3 channels (grayscale to BGR)
    colored_wave_frame = cv2.cvtColor(normalized_wave_frame, cv2.COLOR_GRAY2BGR)

    # Resize the frame if necessary
    colored_wave_frame = cv2.resize(colored_wave_frame, (500, 500))

    # Write the frame to the video
    out.write(colored_wave_frame)

# Release the VideoWriter
out.release()

print(f"Video saved to {output_video_path}")
