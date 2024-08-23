from django.db import models
from django.conf import settings
from core.models import *

class SubscriptionInfos(models.Model):
    type = models.CharField(max_length=255)
    max_employee_numbers = models.IntegerField()
    max_request_rate = models.IntegerField()
    price = models.IntegerField()
    role = models.ForeignKey(Role, on_delete=models.PROTECT)


class Subscriptions(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    subscriptionInfo = models.ForeignKey(SubscriptionInfos, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()


    

class payment(models.Model):
    subscription = models.ForeignKey(Subscriptions, on_delete=models.PROTECT)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=255)