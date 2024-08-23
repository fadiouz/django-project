import cv2
import os

# Specify the folder containing the frames and the output video file
folder_path = 'scan/'
output_video = 'output_video.avi'

# Get the list of image files in the folder
image_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg') or f.endswith('.png')]
image_files.sort(key=lambda f: int(os.path.splitext(f)[0]))  # Sort files by numeric order

# Read the first frame to get the frame size
first_frame = cv2.imread(os.path.join(folder_path, image_files[0]))
height, width, layers = first_frame.shape

# Define the codec and create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Use 'XVID' or 'MJPG' for .avi files, 'mp4v' for .mp4 files
video = cv2.VideoWriter(output_video, fourcc, 30, (width, height))  # 30 fps

# Read and write each frame to the video
for file in image_files:
    frame = cv2.imread(os.path.join(folder_path, file))
    video.write(frame)

# Release the video writer
video.release()

print(f"Video saved as {output_video}")
