
# cap = cv2.VideoCapture("https://192.168.137.219:8080/video") ## for mobile camera
cap = cv2.VideoCapture(0) ## for laptop camera

while(True):
    # Load image
    ret,image = cap.read()
    
    #to flip camera (r t l && l t r)
    # image = cv2.flip(image,1)
    image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
   
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    edges = cv2.Canny(gray, 50, 150)

    # Find contours
    # contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # # Filter contours by area and shape
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 1000]

    # Approximate contours
    approxed_contours = [cv2.approxPolyDP(cnt, 0.05*cv2.arcLength(cnt, True), True) for cnt in filtered_contours]
    
    rectangled_contours = Cnt.filter_cnts_basedOn_num(approxed_contours , 4)

    rectangled_contours = [cnt for cnt in approxed_contours if ( compass.check_rectangle_with_ratio(countour=cnt , ratio=0.2 , tolerance=0.05))]
    
    length = len(rectangled_contours)

    rectangled_contours , clusters , L_bottom_points = compass.remove_cnt_duplicates(rectangled_contours ,20)

    rectangles = compass.fix_rectangled_countours(rectangled_contours)
    
    # # Identify paper corners
    # cv2.drawContours(image, rectangled_contours, 0,(0,255,0) , 3)  # Draw green rectangle around paper
    # cv2.drawContours(image, approxed_contours, 0,(0,0,255) , 3)  # Draw green rectangle around paper

    # for cnt in rectangled_contours:
    #     cv2.drawContours(image, [cnt], 0,(0,255,0) , 3)  # Draw green rectangle around paper
        
    # for cluster,L_bottom_point in zip(clusters, L_bottom_points) :
    #     cv2.circle(image,(cluster[0],cluster[1]) , 20 , (50,200,70) , 2)
    #     cv2.circle(image,( L_bottom_point[0], L_bottom_point[1]) , 10 , (50,100,70) , 2)
    #     cv2.rectangle(image , cluster , L_bottom_point,  (0,255,0) , 2 )

    # for rectangle in rectangles:
    #       cv2.rectangle(image , rectangle[0]["L_top_point"] , rectangle[0]['R_bottom_point'],  (0,255,0) , 2 )

    
    sectionsIndeces = np.array([50000]*4)
    for i,rectangle in enumerate(rectangles):
        if(i>3):
            break
        sectionsIndeces[i] = rectangle["L_top_point"][0]
    sectionsIndeces.sort()

    sections = []
    for section in sectionsIndeces: 
        for rectangle in rectangles:
            if(rectangle["L_top_point"][0]==section):
                sections.append(rectangle)


    for i,section in enumerate(sectionsIndeces):
        if(section>2000):
            break
        cv2.putText(image ,f"section {i}" ,(section,100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2 )


    # section_selects = np.array([None]*4)

    for i,sect in enumerate(sections):
        if(i>3):
            break
        cv2.rectangle(image , (sect["L_top_point"][0],sect["L_top_point"][1]) ,(sect["R_bottom_point"][0],sect["R_bottom_point"][1]) ,  (0,255,0) , 2 )


    # for i,sect in enumerate(sections):
    #     if(i>3):
    #         break
    #     start_x = sect["L_top_point"][0]
    #     start_y = sect["L_top_point"][1]
    #     end_x = sect["R_bottom_point"][0]
    #     end_y = sect["R_bottom_point"][1]

    #     section_selects[i]=image[ start_y:end_y,start_x:end_x]

    #     cv2.imshow(f'sect {i} image' , section_selects[i])

    cv2.imshow('Original image s' , image)



    # This command let's us quit with the "q" button on a keyboard. 
    if cv2.waitKey(1) & 0xFF == ord('q') : 
	    break
        
print(image.shape)
cv2.destroyAllWindows()
