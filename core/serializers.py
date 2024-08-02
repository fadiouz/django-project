from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



# class UserCreateSerializer(BaseUserCreateSerializer):
#     class Meta(BaseUserCreateSerializer.Meta):
#         fields = ['id', 'username', 'password',
#                   'email', 'first_name', 'last_name']
        
        
        
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Customize token payload if needed
        return token

class UserCreateSerializer(BaseUserCreateSerializer):
    token = serializers.SerializerMethodField()

    class Meta(BaseUserCreateSerializer.Meta):
        gender = serializers.CharField(required=False)

        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'token', 'gender']

    def get_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return data



class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username',
                  'email', 'first_name', 'last_name']