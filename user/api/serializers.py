from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from user.models import *

User = get_user_model()

class UserLoginSerializer(serializers.ModelSerializer):
     token = serializers.SerializerMethodField()
     class Meta:
         model = User
         fields = ('id','email','token', )

     def get_token(self, user):
         token, created = Token.objects.get_or_create(user=user)
         return token.key

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class UserAddressesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = "__all__"

class UserPhonesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPhone
        fields = "__all__"



class UserRolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = "__all__"

class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"

class ResourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = "__all__"