from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import *
from rest_framework.decorators import action 
from .pagination import *
from .models import *
# from .filters import UserFilter
from .serializers import *
from django.db.models import Count
    # Create your views here.

# class userViewSet(ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     #### to filter on any field only but the field name  
#     filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
#     filterset_class = UserFilter
#     pagination_class = UserPagination
#     search_fields = ['f_name']
#     ordering_fields = ['f_name']
    
#     def get_serializer_context(self):
#         return {'request': self.request}

#     def destroy(self, request, *args, **kwargs):
#         return super().destroy(request, *args, **kwargs)
    
    

class AddressViewSet(ModelViewSet):
    queryset = Address.objects.annotate(
        ### the name addressitem ther are in the user models
        user_count=Count('addressitem')).all()
    serializer_class = AddressSerializer
    pagination_class = AddressPagination

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        ### the name addressitem ther are in the user models
        address_id = kwargs['pk']
        if UserAddress.objects.filter(address_id=address_id).exists():
            return Response({'error': 'Cannot delete this address because it is associated with users.'})
        return super().destroy(request, *args, **kwargs)
    
    
    
class AddressUserViewSet(ModelViewSet):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer
    
    # def get_serializer_context(self):
    #     return {'request': self.request}
    
    # def destroy(self, request, *args, **kwargs):
    #     return super().destroy(request, *args, **kwargs)
    
class CostomerViewSet(ModelViewSet):
    queryset = Costomer.objects.all()
    serializer_class = CostomerSerializer
    
    # IsAuthenticated to privet window
    permission_classes = [IsAuthenticated]
    
    # to fetch data user with auth
    @action(detail=False, methods=['GET', 'PUT'])
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def me(self, request):
        (customer, created) = Costomer.objects.get_or_create(user_id = request.user.id)
        if request.method == 'GET':
            serializer = CostomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CostomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)