from django.http import HttpResponse
import cv2
from django.shortcuts import render
import numpy as np
import time
import os
from rest_framework.response import Response
from django.http import JsonResponse

from Ai.layers.paper_detection import paper_detector
from Ai.layers.paper_detection import paper_alignmentor
from Ai.layers.Template_mapper import sections_selector 
from Ai.layers.questions_extractor import questions_extractor
from Ai.layers.Answer_predictor import answer_extractor


class Revision():
    
    def IsImage(ima, contours):
        model_path = 'Ai/models/check_paper.h5'
        paperdetector = paper_detector.paper_checker(model_path)
        # print(paperdetector)
        isPaper = paperdetector.predict(ima)
        if not isPaper:
            return False, None
        else:
            check , image =  paper_alignmentor.align_paper(ima , contours , 4)

            if(not check):
                return False, None
            
            return True, image
        
        
    def SelectSections(image, contours, sections_num, ratio):
        selector = sections_selector.Selector(duplicate_ratio=30)
        sections , check =  selector.select_sections(image, contours, sections_num, ratio)
        if(not check):
            print("could not extract shapes correctly ")
            return False
        return True, sections
             
        
    def ExtractQuestion(sections, sections_num, expected_questions_num):
        Q_exttractor = questions_extractor.Extractor()
        
        questions = np.array([None]*sections_num)
        for i,section in enumerate(sections):
            if(i>=sections_num):
                break
            if(not type(section) == type(None)):
                questions[i] = Q_exttractor.extract_questions(section,expected_questions_num)
                
        
        return questions
                    
                    
    def PredictAnswer(questions, sections_num):
        results = []
        question_count = 1
        answers = np.array([[None]*25]*4)
        answerExtractor = answer_extractor.Answer_Extractor('Ai/models/check_answer_perdictor.h5')
        for i,section in enumerate(questions):
            if(i>=sections_num):
                break

            if(not type(section) == type(None)):
                for j,question in enumerate(section):
                    answers[i][j] = answerExtractor.predict(question)
                    # print(f'i {i} j {j}')
                    result_str = f'{question_count}:{answers[i][j]}'
                    results.append(result_str)
                    question_count += 1
                    
        
        return results
        
    @staticmethod
    def RevisionImage(img, num_questions):
        nparr = np.frombuffer(img.read(), np.uint8)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        
        # response_data = {'result': 'fadi'}
        
        # ................................. Layer 1 .................................
        # check if this image is an automated paper or not
        
        is_image, image = Revision.IsImage(img_np, contours)
        # ............................... Layer 1 end ...............................
        
        
        
        if is_image:
            
            # ................................. Layer 2 .................................
            # select the sections in the paper
            # input : paper image
            # output : sections images
            
            #new cut image
            image = cv2.resize(image, (450, 620))
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            num_questions_value = num_questions[0]
            
            if num_questions_value <= 25:
                sections_num = 1
                print('sections_num = 1')
            elif num_questions_value <= 50:
                sections_num = 2
                print('sections_num = 2')
            elif num_questions_value <= 75:
                sections_num = 3
                print('sections_num = 3')
            else:
                sections_num = 4
                print('sections_num = 4')
            check_extraction,sections = Revision.SelectSections(image, contours, sections_num, 0.2)
            

            
            if not check_extraction:
                return "could not extract Questions Sections.. please align the paper correctly"
            
            check_extraction,ID_section = Revision.SelectSections(image, contours, 1, 1.5)
            
            if not check_extraction:
                return "could not extract Id Sections.."
            # ............................... Layer 2 end ...............................
                
            
                
            # ................................. Layer 3 .................................
            # extract each individual question
            # input : section image
            # output : individul questions images
            questions = Revision.ExtractQuestion(sections, sections_num, 25)
            
            ids = Revision.ExtractQuestion(ID_section, 1, 6)

            # ............................... Layer 3 end .................................
            
                        
            
            
            # .................................. Layer 4 ..................................
            # predict the answer from solved questionqq
            # input : question image
            # output : selected answer A , B , C , D or E ....Z 
            specific_question_answer = Revision.PredictAnswer(questions, sections_num)
            # ............................... Layer 4 end .................................
            
            
            
            return specific_question_answer
        
        else:
            return 'could not detect a paper Or the paper is not aligned correctly'
        
        
