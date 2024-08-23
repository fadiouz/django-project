import cv2
import time

# Load the image
image = cv2.imread('../Data Set/paper section.jpg')

cv2.rectangle(image , (0,0) ,  (image.shape[1] , image.shape[0]) ,(0,0,0) ,4)

edges = cv2.Canny(image , 50, 150)

# cnts = cv2.findCirclesGrid(edges , (40,40))

cnts,_ = cv2.findContours(edges , cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

i=0
while i< image.shape[0]:
    copy = image.copy()
    cv2.line(copy , (0,i) ,  (image.shape[1] , i) ,(0,0,255) ,1)
    cv2.imshow("image",copy)
    # time.sleep(1)

    i+=1
    if(edges[i ,:].mean()<30):
        cv2.line(image , (0,i) ,  (image.shape[1] , i) ,(0,0,255) ,1)


cv2.imshow("image",image)
cv2.imshow("Canny",edges)


cv2.waitKey(0)
cv2.destroyAllWindows()