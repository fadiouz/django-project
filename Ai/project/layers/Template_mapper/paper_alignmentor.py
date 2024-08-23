import cv2
import numpy as np
import compass

# compass.check_direction()

# cap = cv2.VideoCapture("https://192.168.137.149:8080/video") ## for mobile camera
cap = cv2.VideoCapture(0) ## for laptop camera

while(cap.isOpened()):
    # Load image
    ret,image = cap.read()
    
    #to flip camera (r t l && l t r)
    image = cv2.flip(image,1)
   
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

    # filter the shapes and keeps only squared shapes
    # 
    squared_contours = [cnt for cnt in approxed_contours if (compass.check_square(cnt) and  len(cnt)==4)]

    # additional steps to ease handling the alignment that Ahed coded 
    # 
    squared_contours = [ [i[0] for i in cnt ] for cnt in squared_contours]

    # remove duplicated squares 
    squared_contours = compass.remove_cnt_duplicates(squared_contours)

    # check if the squares detected are 2 
    if(len(squared_contours)!=2):
        text_x = int(image.shape[0]/2) -40 
        text_y = int(image.shape[1]/2) - 40
        cv2.putText(image, '!!! CANNOT DETECT A PAPER !!!', (text_x , text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)


    # check if paper is alignmented verticaly 
    check , horizon = compass.alignment_with_paper(squared_contours , tolerance=30)
    if(check):
        cv2.line(image , horizon[0], horizon[1] , (0,255,0),3)
        print(horizon)
    else:
        cv2.line(image , horizon[0], horizon[1] , (0,255,255),3)
        text_x = int(image.shape[0]/2) -80 
        text_y = int(image.shape[1]/2) - 80
        cv2.putText(image, '!!! please align the paper correctly !!!', (text_x , text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 255, 0), 2)
    
    # Identify paper corners
    for i,cnt in enumerate(squared_contours):
        # cv2.drawContours(image, [cnt], 0,color , 3)  # Draw green rectangle around paper
        # cv2.rectangle(gray , cnt[0][0], cnt[3][0] , (255,0,0),2)
        cv2.line(image , cnt[0], cnt[1] , (0,255,0),2)
        cv2.line(image , cnt[1], cnt[2] , (0,255,0),2)
        cv2.line(image , cnt[2], cnt[3] , (0,255,0),2)
        cv2.line(image , cnt[3], cnt[0] , (0,255,0),2)


    cv2.imshow('canny' , edgesImage)
    cv2.imshow('original image' , image)



    # This command let's us quit with the "q" button on a keyboard. 
    if cv2.waitKey(1) & 0xFF == ord('q') : 
	    break
        

# cv2.waitKey(0)
cv2.destroyAllWindows()


def check_alignment(contours):
    squared_contours = compass.remove_cnt_duplicates(contours)

    check , horizon = compass.alignment_with_paper(squared_contours , tolerance=30)
    
    if(check):
        cv2.line(image , horizon[0], horizon[1] , (0,255,0),3)
    else:
        cv2.line(image , horizon[0], horizon[1] , (0,255,255),3)
        text_x = int(image.shape[0]/2) -80 
        text_y = int(image.shape[1]/2) - 80
        cv2.putText(image, '!!! please align the paper correctly !!!', (text_x , text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 255, 0), 2)
    
    # Identify paper corners
    for i,cnt in enumerate(squared_contours):
        # cv2.drawContours(image, [cnt], 0,color , 3)  # Draw green rectangle around paper
        # cv2.rectangle(gray , cnt[0][0], cnt[3][0] , (255,0,0),2)
        cv2.line(image , cnt[0], cnt[1] , (0,255,0),2)
        cv2.line(image , cnt[1], cnt[2] , (0,255,0),2)
        cv2.line(image , cnt[2], cnt[3] , (0,255,0),2)
        cv2.line(image , cnt[3], cnt[0] , (0,255,0),2)