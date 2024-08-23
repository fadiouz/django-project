from django.urls import path
from rest_framework.routers import DefaultRouter 
from . import views


#URLConf

router= DefaultRouter()
router.register('address-users', views.AddressUserViewSet)
router.register('addresses', views.AddressViewSet)
router.register('costomers', views.CostomerViewSet)


urlpatterns = router.urls