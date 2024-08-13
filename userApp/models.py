from django.db import models
from django.conf import settings


class Classes(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)


class Students(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    father = models.CharField(max_length=255)
    mother = models.CharField(max_length=255)
    
    
class StudentClasses(models.Model):
    classes = models.ForeignKey(Classes, on_delete=models.PROTECT)
    student = models.ForeignKey(Students, on_delete=models.PROTECT)
    examination_id = models.CharField(max_length=255)
    date = models.DateField()
    

class Exams(models.Model):
    classes = models.ForeignKey(Classes, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    complete_mark = models.IntegerField()
    pass_mark = models.IntegerField()
    question_number = models.IntegerField()
    

class ExamForms(models.Model):
    exam = models.ForeignKey(Exams, on_delete=models.PROTECT)
    form_name = models.CharField(max_length=255)
    

class questions(models.Model):
    examForm = models.ForeignKey(ExamForms, on_delete=models.PROTECT)
    question_number = models.IntegerField(max_length=10)
    answer = models.CharField(max_length=10)
    
class Marks(models.Model):
    studentClass = models.ForeignKey(StudentClasses, on_delete=models.PROTECT)
    xamForm = models.ForeignKey(ExamForms, on_delete=models.PROTECT)
    mark = models.IntegerField()
    status = models.CharField(max_length=50)
