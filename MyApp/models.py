from django.db import models

# Create your models here.
class Address (models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    

    
class User (models.Model):
    f_name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255, unique=True)
    address = models.ForeignKey(Address, on_delete=models.PROTECT)

    


