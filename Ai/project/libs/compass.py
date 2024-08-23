import cv2
import numpy as np

def check_direction():
    pass


# this method returns the point with the biggest x+y value
# which means returns the right-bottom corner point of a square
def max_point(points):
    max = points[0]
    for point in points:
        if ((point[0]+point[1])>(max[0]+max[1])):
            max = point
    return max

def max_Y_point(points):
    max = points[0]
    for point in points:
        if (point[1]>max[1]):
            max = point
    return max

def max_X_point(points):
    max = points[0]
    for point in points:
        if (point[0]>max[0]):
            max = point
    return max

def min_Y_point(points):
    min = points[0]
    for point in points:
        if (point[1]<min[1]):
            min = point
    return min

def min_X_point(points):
    min = points[0]
    for point in points:
        if (point[0]<min[0]):
            min = point
    return min


# this method returns the point with the biggest x+y value
# which means returns the right-bottom corner point of a square
def min_point(points):
    min = points[0]
    for point in points:
        if ((point[0]+point[1])<min[0]+min[1]):
            min = point
    return min

def min_Y_point(points):
    min = points[0]
    for point in points:
        if (point[1]<min[1]):
            min = point
    return min

# this methode aprrox a contour closed to a rectangle shape into exact rectangle
# this dunctions returns two points represents the rectangle of a rectangled contours
def fix_rectangled_countours(contrs ):
    formated_contrs = [ [i[0] for i in cnt ] for cnt in contrs]
    rectangles = []
    for formated_cnt in formated_contrs:
        if(type(formated_cnt[0]) != type(np.array([0,0]))):
            break
        l_top_point = (min_X_point(formated_cnt)[0] , min_Y_point(formated_cnt)[1] )
        r_bottom_point = (max_X_point(formated_cnt)[0] , max_Y_point(formated_cnt)[1] )

        rectangles.append({"L_top_point":l_top_point ,"R_bottom_point":r_bottom_point })

    return rectangles

# check if some point is close to a point within a squared reange
def in_squared_range(center, dist ,point):
    return ( abs(point[0]-center[0])<dist and abs(point[1]-center[1])<dist )

def is_point_in_clusters(clusters , point , range=10):
    for cluster in clusters:
        if(in_squared_range(cluster , range , point)):
            return True
    return False

def remove_cnt_duplicates(contrs , range):
    formated_contrs = [ {'cnt':[i[0] for i in cnt ]   , "R_bottom_point": (0,0) } for cnt in contrs]
    clusters = []
    L_bottom_points=[]
    cnts = []
    for i,formated_cnt in enumerate(formated_contrs):
        if(type(formated_cnt['cnt'][0]) != type(np.array([0,0]))):
            break
        formated_cnt["R_bottom_point"] = max_point(formated_cnt['cnt'])
        L_b_point = min_point(formated_cnt['cnt'])
        if (not is_point_in_clusters(clusters=clusters , point=formated_cnt["R_bottom_point"]  , range=range)):
            cnts.append(contrs[i])
            clusters.append(formated_cnt["R_bottom_point"])
            L_bottom_points.append(L_b_point)

    return cnts , clusters ,L_bottom_points

def alignment_with_paper(contours , tolerance = 4):
    R_bottom_points = np.array([(0,0)]*len(contours))
    for i,cnt in enumerate(contours):
        R_bottom_points[i] = max_point(cnt)

    i=0
    while (i<len(R_bottom_points)):
        j=i+1
        while j<len(R_bottom_points):
            if(is_point_on_line(0,R_bottom_points[i][1] ,R_bottom_points[j][0] ,R_bottom_points[j][1] , tolerance)):
                return True ,[R_bottom_points[i] , R_bottom_points[j]]
            j+=1
        i+=1
    return False,[(0,0),(0,0)]
            

# line's formula :
#  y = ax + c
def is_point_on_line(a , c , x, y,tolerance=3 ):
    # point has this form : (x , y)
    expected_y= a*x + c
    return abs(expected_y - y) < tolerance

# check if the countour formed a square 
def check_square(countour):
    _,_, w, h = cv2.boundingRect(countour)
    ratio = float(w)/h
    return ratio >= 0.9 and ratio <= 1.1
     
def check_rectangle_with_ratio(countour , ratio , tolerance=0.1):
    _,_, w, h = cv2.boundingRect(countour)
    cnt_ratio = float(w)/h
    return cnt_ratio >= ratio-tolerance and cnt_ratio <= ratio+tolerance
     
