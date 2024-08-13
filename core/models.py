from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# Create your models here.

class User(AbstractUser):
    first_name = None
    last_name = None
    email = models.EmailField(unique=True)
    phone_number = models.IntegerField(unique=True)


class Addresses(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.PROTECT)
    
    def __str__(self):
        return self.name
    
class BusinessAcounts(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    address = models.ManyToManyField(Addresses)
    


class Imployees(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    business_acounts = models.ForeignKey(BusinessAcounts, on_delete=models.PROTECT)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)


class Customers(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.ManyToManyField(Addresses)
    
