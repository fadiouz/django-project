from django.urls import path
from .views import *
from . import views


urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
]

