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


    # Define the kernel size and type
    kernel = np.ones((5, 5), np.uint8)
    # Apply erosion
    min_filtered = cv2.erode(gray, kernel)
 
    kernel = np.ones((3,3),np.float32)/9
    smoothedafter_min = cv2.filter2D(min_filtered,-1,kernel)


    _,threshmin_filtered = cv2.threshold(min_filtered,150,255,0)
    _,threshsmoothmin_filtered = cv2.threshold(smoothedafter_min,150,255,0)



    cv2.imshow(' min_filtered_blue', threshmin_filtered )
    cv2.imshow('smooth after min filtered Detection', threshsmoothmin_filtered )


    # This command let's us quit with the "q" button on a keyboard. 
    if cv2.waitKey(1) & 0xFF == ord('q') : 
	    break
        
print(gray)
print(grayblue)
# cv2.waitKey(0)
cv2.destroyAllWindows()
