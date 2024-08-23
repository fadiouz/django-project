import cv2
import numpy as np
from ...libs import compass as compass
from ...libs import contour as Cnt

class Selector:
    def __init__(self  , duplicate_ratio=20):
        self.duplicate_ratio=duplicate_ratio
        pass

    def select_sections(self ,paper_image , contours , sections_number=4):
        # # Filter contours by area and shape
        filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 1000]

        # Approximate contours
        approxed_contours = [cv2.approxPolyDP(cnt, 0.05*cv2.arcLength(cnt, True), True) for cnt in filtered_contours]
        
        rectangled_contours = Cnt.filter_cnts_basedOn_num(approxed_contours , 4)

        # for rect in rectangled_contours:
        #     cv2.drawContours(paper_image ,[rect],0 ,(222,0,0) ,2)

        rectangled_contours = [cnt for cnt in rectangled_contours if ( compass.check_rectangle_with_ratio(countour=cnt , ratio=0.2 , tolerance=0.05))]

        rectangled_contours , clusters , _ = compass.remove_cnt_duplicates(rectangled_contours ,self.duplicate_ratio)
     
        rectangles = compass.fix_rectangled_countours(rectangled_contours)

        sectionsIndeces = np.array([50000]*sections_number)
        for i,rectangle in enumerate(rectangles):
            if(i>=sections_number):
                break
            sectionsIndeces[i] = rectangle["L_top_point"][0]
        sectionsIndeces.sort()

        sections = []
        for section in sectionsIndeces: 
            for rectangle in rectangles:
                if(rectangle["L_top_point"][0]==section):
                    sections.append(rectangle)

        section_selects = np.array([None]*4)

        for i,sect in enumerate(sections):
            if(i>=sections_number):
                break
            start_x = sect["L_top_point"][0]
            start_y = sect["L_top_point"][1]
            end_x = sect["R_bottom_point"][0]
            end_y = sect["R_bottom_point"][1]
            section_selects[i]=paper_image[start_y:end_y,start_x:end_x]
        

        return section_selects;

    def debug(self , image , rectangles , clusters):
        for rectangle in rectangles:
            cv2.rectangle(image, rectangle["L_top_point"] , rectangle["R_bottom_point"] ,(0,255,0) , 2 )

        for cluster in clusters:
            cv2.circle(image , cluster,20 ,(33,55,88) ,2 )

        cv2.imshow("s" , image[400:])
 