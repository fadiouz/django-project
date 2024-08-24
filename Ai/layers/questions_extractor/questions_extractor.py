import cv2
import numpy as np

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
    
class Extractor():
    def __init__(self):
        self.line_factor=20
        pass
    def extract_questions(self , section_Image , expected_questions_num=25):
        edges = cv2.Canny(section_Image , 50, 150)

        start = 0
        end =5
        lines=[]
        scanner = Scanner()

        # this scans the image and add lines between questions 
        # it has a pronciple similar to Finite Automata FA
        # lines here is used to store indeces of the lines across the y axis

        for i in range(0,section_Image.shape[0]):
            if(edges[i ,:].mean()<self.line_factor):
                scanner.moveTonext_state("s1")
                end=i
            else:
                scanner.moveTonext_state("s0")
                if(scanner.status_changed(From="s1" , To="s0")):
                    lines.append(int((start+end)/2))
                start=i

        # self.debug(section_Image , lines)
        
        if(len(lines)<expected_questions_num):
            raise  Exception("Sorry, could not scan the paper properly")
        
        
        # self.debug(section_Image , lines)

        # this code selects the questions rectangles based on the lines specified 
        # it assign the selected area of the qustion to its index element in the qustions np array
        questions = np.array([None]*expected_questions_num)
        fails=0
        for i in range(1 ,len(lines)):
            if(i-fails>expected_questions_num):
                break
            if(abs(lines[i-1]-lines[i])<section_Image.shape[0]/40):
                fails +=1
                continue
            questions[i-fails-1]=section_Image[lines[i-1]:lines[i] ,:]

        return questions

    def debug(self , image ,lines):
        section_Image = image.copy()
        for i in lines:
            cv2.line(section_Image , (0,i) ,  (section_Image.shape[1] , i) ,(0,0,255) ,1)
        
        print(len(lines))
        cv2.imshow("s" , section_Image)
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
