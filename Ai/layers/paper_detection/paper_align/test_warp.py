import cv2
import numpy as np
import libs.compass as compass
import libs.contour as Cnt




image = cv2.imread('final paper.jpg')

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

edgesImage = cv2.Canny(gray, 50, 150)

# Find contours
# contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours, _ = cv2.findContours(edgesImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# # Filter contours by area and shape
# remove contors with less than 500 pixel area
filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 500]

# Approximate contours
# aprocimate cotours to polygons shapes
approxed_contours = [cv2.approxPolyDP(cnt, 0.1*cv2.arcLength(cnt, True), True) for cnt in filtered_contours]

rectangled_contours = Cnt.filter_cnts_basedOn_num(approxed_contours , 4)

# for rect in rectangled_contours:
#     cv2.drawContours(paper_image ,[rect],0 ,(222,0,0) ,2)

squared_contours = [cnt for cnt in rectangled_contours if ( compass.check_rectangle_with_ratio(countour=cnt , ratio=1 , tolerance=0.05))]

# remove duplicated squares 
squared_contours,_,_ = compass.remove_cnt_duplicates(squared_contours , 10)




squared_contours = compass.fix_rectangled_countours(squared_contours)

print(len(squared_contours))
print(squared_contours)


# for rectangle in squared_contours:
#     cv2.rectangle(image, rectangle["L_top_point"] , rectangle["R_bottom_point"] ,(0,255,0) , 2 )


# check if the squares detected are 2 
if(len(squared_contours)!=3):
    text_x = int(image.shape[0]/2) -40 
    text_y = int(image.shape[1]/2) -40
    cv2.putText(image, '!!! CANNOT DETECT A PAPER !!!', (text_x , text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)


# check if paper is alignmented verticaly 
check , horizon = compass.alignment_with_paper2(squared_contours , tolerance=30)


if(check):
    cv2.line(image , horizon[0], horizon[1] , (0,255,0),3)
    print(horizon)
else:
    cv2.line(image , horizon[0], horizon[1] , (0,255,255),3)
    text_x = int(image.shape[0]/2) -80 
    text_y = int(image.shape[1]/2) - 80
    cv2.putText(image, '!!! please align the paper correctly !!!', (text_x , text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 255, 0), 2)


for rectangle in squared_contours:
    cv2.rectangle(image, rectangle["L_top_point"] , rectangle["R_bottom_point"] ,(0,255,0) , 2 )


# # Identify paper corners
# for i,cnt in enumerate(squared_contours):
#     # cv2.drawContours(image, [cnt], 0,(0,255,0) , 3)  # Draw green rectangle around paper
#     # cv2.rectangle(gray , cnt[0][0], cnt[3][0] , (255,0,0),2)
#     cv2.line(image , cnt[0], cnt[1] , (0,255,0),2)
#     cv2.line(image , cnt[1], cnt[2] , (0,255,0),2)
#     cv2.line(image , cnt[2], cnt[3] , (0,255,0),2)
#     cv2.line(image , cnt[3], cnt[0] , (0,255,0),2)


cv2.imshow('original image' , image)
cv2.imshow('original image2' , image[-200 : ])


cv2.waitKey(0)
cv2.destroyAllWindows()
    

