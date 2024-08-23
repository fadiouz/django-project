from django.urls import path
from rest_framework.routers import DefaultRouter 
from . import views
from .views import ImageView

router = DefaultRouter()
router.register('exams', views.ExamsViewSet)
router.register('classes', views.ClassesViewSet)
router.register('questionsExamForms', views.QuestionsExamFormsViewSet)

urlpatterns = [
    path('images/', ImageView.as_view(), name='image-api'),
]

urlpatterns += router.urls  # دمج نمط العناوين الخاص بالـ router مع نمط العناوين العام