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
        
        
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Customize token payload if needed
        return token

class UserCreateSerializer(BaseUserCreateSerializer):
    token = serializers.SerializerMethodField()
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)

    class Meta(BaseUserCreateSerializer.Meta):

        fields = ['id', 'username', 'password', 'email', 'phone_number', 'token', 'first_name', 'last_name']

    def get_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return data

    def create(self, validated_data):
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')

        user = get_user_model().objects.create_user(**validated_data)
        Customers.objects.create(user=user, first_name=first_name, last_name=last_name)
        return user

