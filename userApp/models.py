from django.db import models
from django.conf import settings
from datetime import date

class Classes(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

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
    title = models.CharField(max_length=255)
    complete_mark = models.IntegerField()
    pass_mark = models.IntegerField()
    question_number = models.IntegerField()
    date = models.DateField(default=date.today)
    
    def __str__(self):
        return self.title

class ExamForms(models.Model):
    exam = models.ForeignKey(Exams, on_delete=models.CASCADE)
    form_name = models.CharField(max_length=255)
    

class Questions(models.Model):
    examForm = models.ForeignKey(ExamForms, on_delete=models.CASCADE)
    question_id = models.IntegerField(null=True)
    answer = models.CharField(max_length=1)
    
    def save(self, *args, **kwargs):
        self.answer = self.answer.upper()
        super(Questions, self).save(*args, **kwargs)
        
        
class Marks(models.Model):
    studentClass = models.ForeignKey(StudentClasses, on_delete=models.PROTECT)
    xamForm = models.ForeignKey(ExamForms, on_delete=models.PROTECT)
    mark = models.IntegerField()
    status = models.CharField(max_length=50)
