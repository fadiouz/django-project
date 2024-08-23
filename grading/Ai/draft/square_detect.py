import cv2
import numpy as np


# cap = cv2.VideoCapture("https://192.168.137.43:8080/video") 
cap = cv2.VideoCapture(0) 

while(cap.isOpened()):
    # Load image
    ret,image = cap.read()

    # image = cv2.rotate(image , cv2.ROTATE_90_CLOCKWISE)
    # size = (400,600)
    # image= cv2.resize(image , size)



    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    ret,thresh = cv2.threshold(gray,120,255,0)

    kernel = np.ones((5,5),np.float32)/25
    smoothed = cv2.filter2D(gray,-1,kernel)
    smoothed = cv2.filter2D(smoothed,-1,kernel)
 

    # Find contours
    # contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter contours by area and shape
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 1000]

    # Approximate contours
    approx_contours = [cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True) for cnt in filtered_contours]

    # Identify paper corners
    for  i,cnt in enumerate(approx_contours):
        color = (i*20, 200-i*5, 0)
        cv2.drawContours(image, [cnt], 0,color , 3)  # Draw green rectangle around paper

    # Display result
    
    cv2.imshow('Paper Detection', image)
    cv2.imshow('ffr Detection', thresh )
    cv2.imshow('gr Detection', smoothed )

    # This command let's us quit with the "q" button on a keyboard. 
    if cv2.waitKey(1) & 0xFF == ord('q') : 
	    break

# cv2.waitKey(0)
cv2.destroyAllWindows()
