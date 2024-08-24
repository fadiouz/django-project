from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from core.models import *
from core.serializers import *
from django.contrib.auth import get_user_model
from .models import *
from django.conf import settings
from rest_framework.response import Response

   
class GetNameClassesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)  
    name = serializers.CharField(read_only=True)  
    
    class Meta:
        model = Classes
        fields = ['id', 'name']
          
   
class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classes
        fields = ['id', 'first_name', 'last_name', 'father', 'mother']  
    
    
class StudentClassesSerializer(serializers.ModelSerializer):
    classes = GetNameClassesSerializer()
    student = StudentsSerializer()
    class Meta:
        model = Classes
        fields = ['id', 'classes', 'student', 'examination_id', 'date']  
    
        
class ExamsSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=False)
    complete_mark = serializers.IntegerField(required=False)
    question_number = serializers.IntegerField(required=False)
    classes_id = serializers.IntegerField(required=False)

    classes = GetNameClassesSerializer(read_only=True)
    classes_id = serializers.PrimaryKeyRelatedField(queryset=Classes.objects.all(), write_only=True)
    # exam_forms = ExamFormsSerializer(many=True, write_only=True)
    
    class Meta:
        model = Exams
        fields = ['id', 'title', 'complete_mark', 'pass_mark', 'question_number', 'classes_id', 'classes', 'date']
    
    # def get_forms(self, obj):
    #     exam_forms = ExamForms.objects.filter(exam=obj)
    #     serializer = GetNameExamFormsSerializer(exam_forms, many=True)
    #     return serializer.data
    
    def create(self, validated_data):
        classes_id = validated_data.pop('classes_id')
        # exam_forms_data = validated_data.pop('exam_forms')
        exam = Exams.objects.create(classes=classes_id, **validated_data)
        
        # for exam_form_data in exam_forms_data:
        #     ExamForms.objects.create(exam=exam, **exam_form_data)
            
        return exam
    
    # def update(self, instance, validated_data):
    #     classes_id = validated_data.get('classes_id')
    #     if classes_id:
    #         instance.classes_id = classes_id
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)

    #     instance.save()
    #     return instance


class QuestionsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)  
    question_id = serializers.IntegerField()  
    answer = serializers.CharField() 
    class Meta:
        model = Questions
        fields = ['id', 'question_id', 'answer']
        

class GetNameQuestionsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)  
    question_id = serializers.IntegerField(read_only=True) 
    answer = serializers.CharField(read_only=True) 

    class Meta:
        model = Questions
        fields = ['id', 'question_id', 'answer'] 
             

class QuestionsExamFormsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    form_name = serializers.CharField() 
    questions = QuestionsSerializer(many=True, write_only=True)
    exam_id = serializers.PrimaryKeyRelatedField(queryset=Exams.objects.all())
    
    class Meta:
        model = ExamForms
        fields = ['id', 'form_name', 'exam_id', 'questions']
        
    def get_questions(self, obj):
        questions = Questions.objects.filter(examForm=obj)
        serializer = GetNameQuestionsSerializer(questions, many=True)
        return serializer.data
    
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['questions'] = self.get_questions(instance)
        return ret
    
    
    def update(self, instance, validated_data):
        exam_id = validated_data.get('exam_id')
        questions_data = validated_data.pop('questions')

        if exam_id:
            instance.exam_id = exam_id

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if questions_data:
            # Update or create questions
            for question_data in questions_data:
                question_id = question_data.get('id', None)
                if question_id:
                    question = Questions.objects.get(pk=question_id)
                    question.answer = question_data.get('answer')
                    question.save()
                else:
                    Questions.objects.create(examForm=instance, **question_data)

        return instance
    
    def delete(self, instance):
        questions_to_delete = Questions.objects.filter(examForm=instance)
        questions_to_delete.delete()
        instance.delete()
    
    
class getQuestionsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)  
    question_id = serializers.IntegerField(read_only=True)  
    answer = serializers.CharField(read_only=True) 
    
    class Meta:
        model = Questions
        fields = ['id', 'question_id', 'answer']


