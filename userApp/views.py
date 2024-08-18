from rest_framework.response import Response
from .serializers import *
from core.models import *
from rest_framework.viewsets import ModelViewSet
from .pagination import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action 
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404


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

    def update(self, request, *args, **kwargs):
        exam_id = kwargs.get('pk')
        if ExamForms.objects.filter(exam=exam_id).exists():
            title = request.data.get('title')
            exam = Exams.objects.get(pk=exam_id)
            exam.title = title
            exam.save()
            
            return Response({"message": "Only title changed."},
                        status=status.HTTP_200_OK)
        else:
            title = request.data.get('title')
            complete_mark = request.data.get('complete_mark')
            question_number = request.data.get('question_number')
            pass_mark = request.data.get('pass_mark')
            classes_id = request.data.get('classes_id')
            
            exam = Exams.objects.get(pk=exam_id)
            exam.title = title
            exam.complete_mark = complete_mark
            exam.question_number = question_number
            exam.pass_mark = pass_mark
            exam.classes_id = classes_id
            exam.save()
            
            classes = Classes.objects.get(id=classes_id)
    
            serialized_exam = {
                'id': exam.id,
                'title': exam.title,
                'complete_mark': exam.complete_mark,
                'pass_mark': exam.pass_mark,
                'question_number': exam.question_number,
                'classes': {
                    'id': classes.id,
                    'name': classes.name
                }
            }
            
            return Response(serialized_exam, status=status.HTTP_200_OK)


class QuestionsExamFormsViewSet(ModelViewSet):
    queryset = ExamForms.objects.all()
    serializer_class = QuestionsExamFormsSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET', 'PUT', 'POST'])
    def get_queryset(self):
        user = self.request.user
        class_ids = Classes.objects.filter(user=user).values_list('id', flat=True)
        
        if class_ids:
            exam_ids = Exams.objects.filter(classes_id__in=class_ids).values_list('id', flat=True)
            return ExamForms.objects.filter(exam_id__in=exam_ids)
        else:
            return ExamForms.objects.none()
          
    def create(self, request, *args, **kwargs):
        exam_id = request.data.get('exam_id')
        questions = request.data.get('questions', [])
        question_enter_number = len(questions)

        exam = get_object_or_404(Exams, pk=exam_id)
        question_number = exam.question_number

        if question_number != question_enter_number:
            raise serializers.ValidationError("Number of questions doesn't match the required number for this exam.")

        examForm = ExamForms.objects.create(exam=exam, form_name=request.data.get('form_name'))

        question_list = []
        for question_data in questions:
            question = Questions.objects.create(examForm=examForm, **question_data)
            question_dict = {
                'id': question.id,
                'question_id': question.question_id,
                'answer': question.answer
            }
            question_list.append(question_dict)

        examForm_dict = {
            'id': examForm.id,
            'exam_id': examForm.exam_id,
            'form_name': examForm.form_name,
            'questions': question_list
        }

        return Response(examForm_dict, status=status.HTTP_201_CREATED)


class ClassesViewSet(ModelViewSet):
    queryset = Classes.objects.all()
    serializer_class = GetNameClassesSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['GET'])
    def get_queryset(self):
        return Classes.objects.filter(user=self.request.user)
    
   
    def retrieve(self, request, *args, **kwargs):
        additional_data = []
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
    
    
class ImageView(APIView):
    def post(self, request):
        exam_id = request.data.get('exam_id')
        if 'image' in request.FILES:
            image_data = request.FILES['image']
            
            resposne = {
                'image': str(image_data),
                'exam_id': exam_id,
            }
            
            return Response({'resposne': resposne}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)