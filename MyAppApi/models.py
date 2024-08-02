from django.db import models
from django.conf import settings


# Create your models here.
class Address (models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
        
    ##### to return the city in the serializers
    def __str__(self) -> str:
        return self.city 

    
class UserAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='addressitem')
    num = models.CharField(max_length=255)
    
    

# to add another field to user table
class Costomer (models.Model):
    gender = models.CharField(max_length=255)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


