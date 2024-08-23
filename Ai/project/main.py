import cv2
import numpy as np
import time

from layers.Template_mapper import sections_selector 
from layers.questions_extractor import questions_extractor
from layers.paper_detection import paper_detector
from layers.Answer_predictor import answer_extractor

image = cv2.imread('Data/paper5.jpg')

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(gray, 50, 150)

# Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# ................................. Layer 1 .................................
# check if this image is an automated paper or not
start_time = time.time()
model_path = 'models\check_paper.h5'
paperdetector = paper_detector.paper_checker(model_path)
isPaper = paperdetector.predict(image)

if(not isPaper):
    print("this image is not a paper")
    exit()

end_time = time.time()
execution_time = end_time - start_time

print(f"Execution time - Layer1 check paper: {execution_time} seconds")


# ............................... Layer 1 end ...............................


# ................................. Layer 2 .................................
# select the sections in the paper
# input : paper image
# output : sections images

start_time = time.time()
selector = sections_selector.Selector(duplicate_ratio=30)
sections =  selector.select_sections(image , contours , 4)

end_time = time.time()
execution_time = end_time - start_time

print(f"Execution time - Layer 2 select sections: {execution_time} seconds")

print(sections)
# ............................... Layer 2 end ...............................


# ................................. Layer 3 .................................
# extract each individual question
# input : section image
# output : individul questions images
start_time = time.time()
Q_exttractor = questions_extractor.Extractor()

questions = np.array([None]*4)
for i,section in enumerate(sections):
    if(not type(section) == type(None)):
        questions[i] = Q_exttractor.extract_questions(section,expected_questions_num=25)

end_time = time.time()
execution_time = end_time - start_time

print(f"Execution time - Layer 3 extract questions: {execution_time} seconds")


# ............................... Layer 3 end .................................



# .................................. Layer 4 ..................................
# predict the answer from solved questionqq
# input : question image
# output : selected answer A , B , C , D or E ....Z 

start_time = time.time()

answers = np.array([[None]*25]*4)
answerExtractor = answer_extractor.Answer_Extractor('models\check_answer_perdictor.h5')
for i,section in enumerate(questions):
    if(not type(section) == type(None)):
        for j,question in enumerate(section):
            answers[i][j] = answerExtractor.predict(question)
            # answers[i][j] = answerExtractor.lite_predict(np.array(question , dtype=np.float32))


end_time = time.time()
execution_time = end_time - start_time

print(f"Execution time - layer 4 answer extractor: {execution_time} seconds")

# ................................ Layer 4 end ................................


cv2.imshow(f"question {answers[0][1]}" , questions[0][1])

cv2.waitKey(0)
cv2.destroyAllWindows()
    