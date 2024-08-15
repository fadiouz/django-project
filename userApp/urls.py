from django.urls import path
from rest_framework.routers import DefaultRouter 
from . import views


#URLConf

router= DefaultRouter()
# router.register('addresses', views.AddressViewSet)
router.register('exams', views.ExamsViewSet)
router.register('classes', views.ClassesViewSet)


urlpatterns = router.urls