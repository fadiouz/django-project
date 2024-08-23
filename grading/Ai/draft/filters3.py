import cv2
import numpy as np


<<<<<<< HEAD
# cap = cv2.VideoCapture("https://192.168.1.34:8080/video") ## for mobile camera
cap = cv2.VideoCapture(0) ## for laptop camera
=======
cap = cv2.VideoCapture("http://192.168.1.35:8080/video") ## for mobile camera
# cap = cv2.VideoCapture(0) ## for laptop camera
>>>>>>> 8c25210ab7115df9fc9e9960b37b7c2f9d6f6506

# Grayscale Intensity values to convert from RGB to grayscale
# original values [B = [0.114] , G = [0.299] , R = [0.587]]
CUSTOME_BGR2GRAY =np.array([[0.587] ,[0.299],[0.0]])

while(cap.isOpened()):
    # Load image
    ret,image = cap.read()
    
    #to flip camera (r t l && l t r)
<<<<<<< HEAD
    image = cv2.flip(image,1)
=======
    # image = cv2.flip(image,1)
    image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

>>>>>>> 8c25210ab7115df9fc9e9960b37b7c2f9d6f6506
   
    # Convert to grayscale
    gray =  np.dot(image[:,:] , CUSTOME_BGR2GRAY )
    gray = gray.reshape((gray.shape[0],gray.shape[1]))
    # Convert the result to integer values
    gray = gray.astype(np.uint8)

    
    # Define the kernel size and type
    kernel = np.ones((5, 5), np.uint8)
    # Apply erosion
    min_filtered = cv2.erode(gray, kernel)
 
    kernel = np.ones((3,3),np.float32)/9
    smoothedafter_min = cv2.filter2D(min_filtered,-1,kernel)

    # Apply edge detection
    edges = cv2.Canny(smoothedafter_min, 50, 150)


    _,threshmin_filtered = cv2.threshold(min_filtered,150,255,0)
    _,threshsmoothmin_filtered = cv2.threshold(smoothedafter_min,120,255,0)

        # Find contours
    # contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter contours by area and shape
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 500]

    # Approximate contours
    approx_contours = [cv2.approxPolyDP(cnt, 0.1*cv2.arcLength(cnt, True), True) for cnt in filtered_contours]

    # Identify paper corners
    for  i,cnt in enumerate(approx_contours):
        color = (i*20, 200-i*5, 0)
        cv2.drawContours(gray, [cnt], 0,color , 1)  # Draw green rectangle around paper
        cv2.drawContours(threshsmoothmin_filtered, [cnt], 0,color , 1)  # Draw green rectangle around paper
        if(len(cnt)==4):
            #  cv2.rectangle(gray , cnt[0][0], cnt[3][0] , (255,0,0),2)
             cv2.line(gray , cnt[0][0], cnt[1][0] , (255,0,0),2)
             cv2.line(gray , cnt[1][0], cnt[2][0] , (255,0,0),2)
             cv2.line(gray , cnt[2][0], cnt[3][0] , (255,0,0),2)
    

    cv2.imshow('smooth after min filtered Detection', gray )
    cv2.imshow('filtered Detection', threshmin_filtered )
    cv2.imshow('canny' , edges)



    # This command let's us quit with the "q" button on a keyboard. 
    if cv2.waitKey(1) & 0xFF == ord('q') : 
	    break
        
print(approx_contours[0])

# cv2.waitKey(0)
cv2.destroyAllWindows()
