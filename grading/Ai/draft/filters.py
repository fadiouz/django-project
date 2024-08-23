import cv2
import numpy as np
 
 
# cap = cv2.VideoCapture("https://192.168.137.43:8080/video") 
cap = cv2.VideoCapture(0) 

# Grayscale Intensity values to convert from RGB to grayscale
# original values [B = [0.114] , G = [0.299] , R = [0.587]]
CUSTOME_BGR2GRAY =np.array([[0.587] ,[0.299],[0.0] ] )

while(cap.isOpened()):
    # Load image
    ret,image = cap.read()
    
    image = cv2.flip(image,1)
   
    # Convert to grayscale

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

   
    # blue = np.copy(image)
    # blue[:,:,0]=0
    # blue[:,:,2]=0
    # blue = image[:,:,0]

    grayblue =  np.dot(image[:,:] , CUSTOME_BGR2GRAY )
    grayblue = grayblue.reshape((grayblue.shape[0],grayblue.shape[1]))
    # Convert the result to integer values
    grayblue = grayblue.astype(np.uint8)

    
    kernel = np.ones((4,4),np.float32)/16

    smoothed = cv2.filter2D(gray,-1,kernel)

    # # Define the kernel size and type
    # kernel = np.ones((5, 5), np.uint8)
    # # Apply dilation
    # max_filtered = cv2.dilate(thresh100, kernel)

    # Define the kernel size and type
    kernel = np.ones((5, 5), np.uint8)

    # Apply erosion
    min_filtered = cv2.erode(gray, kernel)
    # min_filtered = cv2.erode(min_filtered, kernel)

    # Apply erosion
    min_filtered_blue = cv2.erode(gray, kernel)
    # min_filtered_blue = cv2.erode(min_filtered, kernel)


    # ret,threshgray = cv2.threshold(gray,100,255,0)
    # ret,threshsmoothed = cv2.threshold(smoothed,100,255,0)
    ret,threshmin_filtered = cv2.threshold(min_filtered,100,255,0)
    ret,threshmin_filtered_blue = cv2.threshold(min_filtered_blue,100,255,0)


    # cv2.imshow('Image', gray)
    # cv2.imshow('Image blue', grayblue)
    
    cv2.imshow('thresh100 min_filtered_blue', min_filtered )
    # cv2.imshow('smoothed gray Detection', threshsmoothed )
    cv2.imshow('thresh100 min filtered Detection', min_filtered_blue )


    # This command let's us quit with the "q" button on a keyboard. 
    if cv2.waitKey(1) & 0xFF == ord('q') : 
	    break
        
print(gray)
print(grayblue)
# cv2.waitKey(0)
cv2.destroyAllWindows()
