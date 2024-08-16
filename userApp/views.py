from rest_framework.response import Response
from .serializers import *
from core.models import *
from rest_framework.viewsets import ModelViewSet
from .pagination import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action 
from rest_framework.exceptions import MethodNotAllowed


class ExamsViewSet(ModelViewSet):
    queryset = Exams.objects.all()
    serializer_class = ExamsSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET', 'PUT', 'POST'])
    def get_queryset(self):
        user = self.request.user
        class_ids = Classes.objects.filter(user=user).values_list('id', flat=True)
        
        if class_ids:
            return Exams.objects.filter(classes_id__in=class_ids)
        else:
            return Exams.objects.none()
        
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        additional_data = []
        
        forms = ExamForms.objects.filter(exam=instance.id).all()
        # forms_serializer = GetNameExamFormsSerializer(forms, many=True)  
        
        for form in forms:
            questions = Questions.objects.filter(examForm=form.id).all()
            question_serializer = getQuestionsSerializer(questions, many=True)
        
            form_data = {
                'id': form.id,
                'form_name': form.form_name,
                'questions': question_serializer.data
            }
            
            additional_data.append(form_data)
        
        serializer = self.get_serializer(instance)
        return Response({**serializer.data, 'forms': additional_data})


class QuestionsExamFormsViewSet(ModelViewSet):
    queryset = ExamForms.objects.all()
    serializer_class = QuestionsExamFormsSerializer
    permission_classes = [IsAuthenticated]

    # @action(detail=False, methods=['GET', 'PUT', 'POST'])
    # def get_queryset(self):
    #     user = self.request.user
    #     class_ids = Classes.objects.filter(user=user).values_list('id', flat=True)
        
    #     if class_ids:
    #         return Exams.objects.filter(classes_id__in=class_ids)
    #     else:
    #         return Exams.objects.none()
        
    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     additional_data = []
        
    #     forms = ExamForms.objects.filter(exam=instance.id).all()
    #     # forms_serializer = GetNameExamFormsSerializer(forms, many=True)  
        
    #     for form in forms:
    #         questions = Questions.objects.filter(examForm=form.id).all()
    #         question_serializer = getQuestionsSerializer(questions, many=True)
        
    #         form_data = {
    #             'id': form.id,
    #             'title': form.form_name,
    #             'questions': question_serializer.data
    #         }
            
    #         additional_data.append(form_data)
        
    #     serializer = self.get_serializer(instance)
    #     return Response({**serializer.data, 'forms': additional_data})



class ClassesViewSet(ModelViewSet):
    queryset = Classes.objects.all()
    serializer_class = GetNameClassesSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['GET'])
    def get_queryset(self):
        return Classes.objects.filter(user=self.request.user)
    
   
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        exams = Exams.objects.filter(classes=instance.id).all()
        exams_serializer = ExamsSerializer(exams, many=True)  
        
        additional_data = {
            'Exams' : exams_serializer.data
        }
        serializer = self.get_serializer(instance)
        return Response({**serializer.data, **additional_data})
    
    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed("POST method is not allowed on this endpoint.")
    
    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT method is not allowed on this endpoint.")
    


# class ExamFormsViewSet(ModelViewSet):
#     queryset = Classes.objects.all()
#     serializer_class = GetNameClassesSerializer
#     permission_classes = [IsAuthenticated]
    
#     @action(detail=False, methods=['GET'])
#     def get_queryset(self):
#         return Classes.objects.filter(user=self.request.user)
    
   
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
        
#         exams = Exams.objects.filter(classes=instance.id).all()
#         exams_serializer = ExamsSerializer(exams, many=True)  
        
#         additional_data = {
#             'Exams' : exams_serializer.data
#         }
#         serializer = self.get_serializer(instance)
#         return Response({**serializer.data, **additional_data})
    
#     def create(self, request, *args, **kwargs):
#         raise MethodNotAllowed("POST method is not allowed on this endpoint.")
    
#     def update(self, request, *args, **kwargs):
#         raise MethodNotAllowed("PUT method is not allowed on this endpoint.")
    