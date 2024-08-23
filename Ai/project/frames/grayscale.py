import cv2 

image = cv2.imread("../Data/edit/paper.jpeg")

grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(image , 50, 150)

cv2.imwrite(f"grayscale.jpg" ,grayscale )
cv2.imwrite(f"canny.jpg" ,edges )