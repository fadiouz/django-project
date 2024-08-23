from django.urls import path
from . import views


#URLConf
urlpatterns = [
    path('test/' , views.say_hello)
]