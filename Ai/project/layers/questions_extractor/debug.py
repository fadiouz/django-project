
import cv2
import numpy as np
# ---------------------------------------------

class Scanner():
    def __init__(self ):
        self.states = ["s0","s1" ,"s2"]
        self.currentstate = 's0'
        self.previous="s0"
    
    def moveTonext_state(self , state):
        self.previous=self.currentstate
        self.currentstate = state

    def status_changed(self ,From , To):
        return self.currentstate==To and self.previous==From
    

# image = cv2.imread('../Data Set/paper section.jpg')

# extractor = Extractor()

# questions = extractor.extract_questions(image)

# cv2.imshow(f"image {questions[24].shape}",questions[24])

# cv2.waitKey(0)
# cv2.destroyAllWindows()






# .......................................................................................




# Load the image
image = cv2.imread('Data/edit/section1.jpg')

edges = cv2.Canny(image , 50, 150)

questions = np.array([None]*26)

scanner = Scanner()
start = 0
end =5
lines=[]
# starts=[]
# ends = []

scan1=0
cimage = image.copy()
for i in range(0,image.shape[0]):
    if(edges[i ,:].mean()<20):
        scanner.moveTonext_state("s1")
        end=i
        copy = cimage.copy()
        cv2.line(copy , (0,i) ,  (image.shape[1] , i) ,(255,0,0) ,1)
        cv2.imwrite(f"frames/scan/{i*2}.jpg" ,copy )

        cv2.line(cimage , (0,i) ,  (image.shape[1] , i) ,(0,255,0) ,1)
        cv2.imwrite(f"frames/scan/{i*2+1}.jpg" , cimage)
    else:
        copy = image.copy()
        cv2.line(copy , (0,i) ,  (image.shape[1] , i) ,(255,0,0) ,1)
        cv2.imwrite(f"frames/scan/{i*2}.jpg" ,copy )

        scanner.moveTonext_state("s0")
        if(scanner.status_changed(From="s1" , To="s0")):
            # print(f"{start} , {end}")
            lines.append(int((start+end)/2))
            cv2.line(image , (0,int((start+end)/2)) ,  (image.shape[1] , int((start+end)/2)) ,(0,0,255) ,1)
            cimage = image.copy()
            # starts.append(start)
            # ends.append(end)
            scan1+=1
        start=i

for i in lines:
    cv2.line(image , (0,i) ,  (image.shape[1] , i) ,(0,0,255) ,1)


# for s ,e in zip(starts , ends):
#     cv2.line(image , (0,s) ,  (image.shape[1] , s) ,(0,255,0) ,1)
#     cv2.line(image , (0,e) ,  (image.shape[1] , e) ,(255,0,0) ,1)

fails=0
for i in range(1 ,len(lines)):
    if(abs(lines[i-1]-lines[i])<image.shape[0]/40):
        fails +=1
        continue
    # cv2.imshow(f"image{i+25-fails}",image[lines[i-1]:lines[i] ,:])
    questions[i-fails-1]=image[lines[i-1]:lines[i] ,:]

cv2.imshow("image 2",questions[2])

cv2.imshow("image",image)

cv2.waitKey(0)
cv2.destroyAllWindows()

