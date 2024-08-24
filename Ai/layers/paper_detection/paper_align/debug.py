import cv2
import numpy as np
import libs.compass as compass
import libs.contour as Cnt

def match_image_with_height(image , new_height = 400):
    # Get the original dimensions of the image
    original_height, original_width = image.shape[:2]

    # Calculate the aspect ratio
    aspect_ratio = original_width / original_height

    # Calculate the new width while maintaining the aspect ratio
    new_width = int(new_height * aspect_ratio)

    # Resize the image
    resized_image = cv2.resize(image, (new_width, new_height))

    return resized_image

def add_text_center(image , text ,color=(255, 255, 255)):
    # Choose the font
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Set the font scale and thickness
    font_scale = 1
    thickness = 3

    # Get the size of the text box (width, height)
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)

    # Calculate the center position for the text
    image_height, image_width = image.shape[:2]
    x = (image_width - text_width) // 2
    y = (image_height + text_height) // 2  # Adding text_height because OpenCV positions text based on the bottom-left corner

    # Put the text on the image
    cv2.putText(image, text, (x, y), font, font_scale, color, thickness, cv2.LINE_AA)

    
def align_papers(image , contours ,border_tolerance=5 ):

    # # Filter contours by area and shape
    # remove contors with less than 500 pixel area
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 500]

    # Approximate contours
    # aprocimate cotours to polygons shapes
    approxed_contours = [cv2.approxPolyDP(cnt, 0.1*cv2.arcLength(cnt, True), True) for cnt in filtered_contours]

    rectangled_contours = Cnt.filter_cnts_basedOn_num(approxed_contours , 4)

    squared_contours = [cnt for cnt in rectangled_contours if ( compass.check_rectangle_with_ratio(countour=cnt , ratio=1 , tolerance=0.2))]

    # remove duplicated squares 
    squared_contours,_,_ = compass.remove_cnt_duplicates(squared_contours , 10)

    # this method approximate a contour which it's shape is close to a rectangle shape into exact rectangle
    squared_contours = compass.fix_rectangled_countours(squared_contours)

    # to draw rectangled contours
    # for rectangle in squared_contours:
    #     cv2.rectangle(image, rectangle["L_top_point"] , rectangle["R_bottom_point"] ,(0,255,0) , 2 )


    # check if the squares detected are 2 
    if(len(squared_contours)!=3):
        add_text_center(image , " CANNOT DETECT PAPER'S BORDERS " , (0,100,255))
        return False , image


    # check if paper is alignmented verticaly 
    check , horizon = compass.alignment_with_paper2(squared_contours , tolerance=30)

    if(not check):
        cv2.line(image , horizon[0], horizon[1] , (0,255,255),3)
        add_text_center(image , "!!! please align the paper correctly !!! " , (0,255,255))

    for rectangle in squared_contours:
        cv2.rectangle(image, rectangle["L_top_point"] , rectangle["R_bottom_point"] ,(0,255,0) , 2 )

    start , end = compass.cut_paper_border(squared_contours)


    tol = border_tolerance
    image = image[start[1]-tol:end[1]+tol ,start[0]-tol:end[0]+tol]

    return check,image

image = cv2.imread('Data/p5.jpg')

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(gray, 50, 150)

# Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

check , image = align_papers(image , contours)

cv2.imshow('original' , image)

cv2.waitKey(0)
cv2.destroyAllWindows()


