from rest_framework import serializers
from .models import *
from django.conf import settings

##### name of serializers first letter must have a capetal
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'street', 'city', 'user_count']
        
    user_count = serializers.IntegerField(read_only=True)
    
    
class UserAddressSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    address_id = serializers.IntegerField()
    
    class Meta:
        model = UserAddress
        fields = ['id', 'address_id', 'user_id', 'num']
        


class CostomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Costomer        
        fields = ['id', 'user_id', 'gender']

# class UserSerializer(serializers.ModelSerializer):
#     address_id = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all(), source='address', write_only=True)
#     address = AddressSerializer(read_only=True)

#         #### this a nother way to return the informatuion
#     class Meta:
#         model = User
#         fields = ['id', 'f_name', 'l_name', 'full_name', 'email', 'phone', 'address', 'address_id']
    
#     def to_internal_value(self, data):
#         ret = super().to_internal_value(data)
#         ret['address'] = self.fields['address_id'].to_internal_value(data['address_id'])
#         return ret
    
#     full_name = serializers.SerializerMethodField(method_name='Fn_with_Ln')
  
    
    
#     def Fn_with_Ln(self, user: User):
#         return user.f_name + ' ' + user.l_name
        
        