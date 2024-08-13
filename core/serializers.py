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


# class UserSerializer(BaseUserSerializer):
#     class Meta(BaseUserSerializer.Meta):
#         model = User
#         fields = ['id', 'username',
#                   'email', 'phone_number']


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']
        
        
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

    class Meta(BaseUserCreateSerializer.Meta):
        model = User        
        fields = ['id', 'username', 'password', 'email', 'phone_number', 'token', 'role', 'role_id']

    def get_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return data

   

