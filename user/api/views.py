from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import UserLoginSerializer
from rest_framework import generics

from user.api.serializers import *

User = get_user_model()

class EmailValidityAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        email = request.data['email']
        user = User.objects.filter(email=email)
        if user:
            return Response({
                'exist': True
            })
        else:
            return Response({
                'exist': False
            })


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_serializer = UserLoginSerializer(user)
        return Response(user_serializer.data, status=200)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

class UsersAPIView(generics.ListAPIView):
    serializer_class = UsersSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset
    
class UserAddressesAPIView(generics.ListAPIView):
    serializer_class = UserAddressesSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = UserAddress.objects.all()
        return queryset
    
class UserPhonesAPIView(generics.ListAPIView):
    serializer_class = UserPhonesSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = UserPhone.objects.all()
        return queryset
    

    
class UserRolesAPIView(generics.ListAPIView):
    serializer_class = UserRolesSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = UserRole.objects.all()
        return queryset
    
class UserPermissionsAPIView(generics.ListAPIView):
    serializer_class = PermissionsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Permission.objects.all()
        return queryset
    
class UserResourcesAPIView(generics.ListAPIView):
    serializer_class = ResourcesSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Resource.objects.all()
        return queryset