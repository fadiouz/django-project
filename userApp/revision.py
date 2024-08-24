from django.http import HttpResponse
import cv2
from django.shortcuts import render
import numpy as np
import time
import os
from rest_framework.response import Response
from django.http import JsonResponse

from Ai.layers.Template_mapper import sections_selector 
from Ai.layers.questions_extractor import questions_extractor
from Ai.layers.paper_detection import paper_detector
from Ai.layers.Answer_predictor import answer_extractor


class Revision():
    def IsImage(image):
        model_path = 'Ai/models/check_paper.h5'
        paperdetector = paper_detector.paper_checker(model_path)
        # print(paperdetector)
        isPaper = paperdetector.predict(image)
        if not isPaper:
            print("This image is not a paper")
            return False  
        else:
            return True
        
        
    def SelectSections(image, contours):
        selector = sections_selector.Selector(duplicate_ratio=30)
        sections =  selector.select_sections(image , contours , 4)
        
        return sections
             
        
    def ExtractQuestion(sections):
        Q_exttractor = questions_extractor.Extractor()
            
        questions = np.array([None]*4)
        for i, section in enumerate(sections):
            if section is not None:
                questions[i] = Q_exttractor.extract_questions(section, expected_questions_num=25)
                
        return questions
                    
                    
    def PredictAnswer(questions):
        results = []
        question_count = 0
        answers = np.array([[None]*25]*4)
        answerExtractor = answer_extractor.Answer_Extractor('Ai/models/check_answer_perdictor.h5')
        for i,section in enumerate(questions):
            if(not type(section) == type(None)):
                for j,question in enumerate(section):
                    answers[i][j] = answerExtractor.predict(question)
                    # print(f'i {i} j {j}')
                    result_str = f'{question_count}:{answers[i][j]}'
                    results.append(result_str)
                    question_count += 1
                    
        
        return results
        
    @staticmethod
    def RevisionImage(image):
        nparr = np.frombuffer(image.read(), np.uint8)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        
        # response_data = {'result': 'fadi'}
        
        # ................................. Layer 1 .................................
        # check if this image is an automated paper or not
        
        is_image = Revision.IsImage(img_np)
        # ............................... Layer 1 end ...............................
        
        
        
        if is_image:
            
            # ................................. Layer 2 .................................
            # select the sections in the paper
            # input : paper image
            # output : sections images
            sections = Revision.SelectSections(img_np, contours)
            # ............................... Layer 2 end ...............................
            
                        
            
            # ................................. Layer 3 .................................
            # extract each individual question
            # input : section image
            # output : individul questions images
            questions = Revision.ExtractQuestion(sections)
            # ............................... Layer 3 end .................................
            
                        
            
            
            # .................................. Layer 4 ..................................
            # predict the answer from solved questionqq
            # input : question image
            # output : selected answer A , B , C , D or E ....Z 
            specific_question_answer = Revision.PredictAnswer(questions)
             # ............................... Layer 4 end .................................
             
             
             
            return specific_question_answer
        
        else:
            return HttpResponse("is not image")
        
        
