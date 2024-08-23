import cv2
import numpy as np


cap = cv2.VideoCapture(0) 

def threshold(x,  start , end ):
     if x<start: return 0
     elif x<end : return 125 
     else: return 255;

while(cap.isOpened()):
    # Load image
    ret,image = cap.read()

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply edge detection
    edges = cv2.Canny(gray, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours by area and shape
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 1000]

    # Approximate contours
    approx_contours = [cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True) for cnt in filtered_contours]

    # Identify paper corners
    for  i,cnt in enumerate(approx_contours):
        color = (i*20, 200-i*5, 0)
        cv2.drawContours(gray, [cnt], 0,color , 3)  # Draw green rectangle around paper

    
    # # Create a mask for pixels less than 85
    # mask_0 = gray < 85

    # # Create a mask for pixels between 85 and 170
    # mask_125 = (gray >= 85) & (gray < 170)

    # # Create a mask for pixels greater than or equal to 170
    # mask_255 = gray >= 170

    # # Apply values based on masks
    # thresome = np.zeros_like(gray)
    # thresome[mask_0] = 0
    # thresome[mask_125] = 125
    # thresome[mask_255] = 255


    # # Apply first threshold to separate the image into two parts
    # _, binary = cv2.threshold(gray, 85, 255, cv2.THRESH_BINARY)
    
    # Display result
    cv2.imshow('Paper Detection', gray)

    # This command let's us quit with the "q" button on a keyboard. 
    if cv2.waitKey(1) & 0xFF == ord('q') : 
	    break

# cv2.waitKey(0)
cv2.destroyAllWindows()
