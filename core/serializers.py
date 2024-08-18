from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *
from django.contrib.auth import get_user_model


# class UserCreateSerializer(BaseUserCreateSerializer):
#     class Meta(BaseUserCreateSerializer.Meta):
#         fields = ['id', 'username', 'password',
#                   'email', 'first_name', 'last_name']


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ['id', 'username',
                  'email', 'phone_number']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addresses
        fields = ['id', 'name', 'parent']
        
      
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']
        
        
        
        
        
class UserAddressSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user_id', write_only=True)
    address_id = serializers.PrimaryKeyRelatedField(queryset=Addresses.objects.all(), source='address_id', write_only=True)
    
    address = AddressSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserAddress
        fields = ['id', 'address_id', 'user_id', 'user', 'address']
        
      
        
              
              
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Customize token payload if needed
        return token




class UserCreateSerializer(BaseUserCreateSerializer):
    token = serializers.SerializerMethodField()
    
    role_id = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), source='role', write_only=True)
    role = RoleSerializer(read_only=True)
    
    # address_id = serializers.PrimaryKeyRelatedField(queryset=Addresses.objects.all(), source='address', write_only=True)
    address = AddressSerializer(read_only=True)


    class Meta(BaseUserCreateSerializer.Meta):
        model = User        
        fields = ['id', 'username', 'password', 'email', 'phone_number', 'token', 'role', 'role_id', 'address']



    def get_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return data

    def create(self, validated_data):
        validated_data['is_active'] = 0 
        user = User.objects.create_user(**validated_data)
        return user

    # def create(self, validated_data):
    #     user = User.objects.create_user(**validated_data)  # إنشاء المستخدم باستخدام البيانات المحققة
    #     token_data = self.get_token(user)  # الحصول على التوكن بعد إنشاء المستخدم
    #     return user
        

        
   

