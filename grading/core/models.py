from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.contrib.auth.models import Permission  

# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=255)
    permission = models.ManyToManyField(Permission)

    def __str__(self):
        return self.name

class Addresses(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True)
    
    def __str__(self):
        return self.name
    
class User(AbstractUser):
    first_name = None
    last_name = None
    email = models.EmailField(unique=True)
    phone_number = models.IntegerField(unique=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.username

class Employees(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='user')
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='employee')


class UserAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    address = models.ForeignKey(Addresses, on_delete=models.CASCADE)


    
