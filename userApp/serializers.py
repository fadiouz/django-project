from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from core.models import *
from core.serializers import *

from django.contrib.auth import get_user_model
from .models import *
from django.conf import settings


    
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
   

class ExamFormsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)  
    form_name = serializers.CharField() 
    class Meta:
        model = ExamForms
        fields = ['id', 'form_name']  
        
        

class GetNameExamFormsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)  
    form_name = serializers.CharField(read_only=True) 
    
    class Meta:
        model = ExamForms
        fields = ['id', 'form_name']  
    
    
        
class ExamsSerializer(serializers.ModelSerializer):
    classes = GetNameClassesSerializer(read_only=True)
    classes_id = serializers.PrimaryKeyRelatedField(queryset=Classes.objects.all(), write_only=True)
    exam_forms = ExamFormsSerializer(many=True, write_only=True)
    # forms = serializers.SerializerMethodField()  
    
    class Meta:
        model = Exams
        fields = ['id', 'title', 'complete_mark', 'pass_mark', 'question_number', 'classes_id', 'classes', 'exam_forms']
    
    # def get_forms(self, obj):
    #     exam_forms = ExamForms.objects.filter(exam=obj)
    #     serializer = GetNameExamFormsSerializer(exam_forms, many=True)
    #     return serializer.data
    
    def create(self, validated_data):
        classes_id = validated_data.pop('classes_id')
        exam_forms_data = validated_data.pop('exam_forms')
        exam = Exams.objects.create(classes=classes_id, **validated_data)
        
        for exam_form_data in exam_forms_data:
            ExamForms.objects.create(exam=exam, **exam_form_data)
            
        return exam
    
    def update(self, instance, validated_data):
        classes_id = validated_data.get('classes_id')
        if classes_id:
            instance.classes_id = classes_id
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance



