import cv2
import numpy as np

# * to access camera stream boradcasted on a URL
# cap = cv2.VideoCapture("https://192.168.137.43:8080/video")

# * to access webcam 
cap = cv2.VideoCapture(0) 

while(cap.isOpened()):
    # Load image
    # capture the current frame from camera and store it as an array
    _,image = cap.read()
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # showing the frame captured 
    cv2.imshow('gray Image', gray)

    # This command let's us quit with the "q" button on a keyboard. 
    if cv2.waitKey(1) & 0xFF == ord('q') : 
	    break

cv2.destroyAllWindows()
