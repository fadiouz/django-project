from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import logout
from .serializers import *
from .models import *
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from .pagination import *


class LogoutView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            try:
                request.user.auth_token.delete()
            except AttributeError:
                pass

            logout(request)
            return Response({"success": "Successfully logged out."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
    def get(self, request):
        return Response({"detail": "Method 'GET' not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    

class AddressViewSet(ModelViewSet):
    queryset = Addresses.objects.annotate().all()
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
