from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from organization.api.serializers import *

class OrganizationsAPIView(generics.ListAPIView):
    serializer_class = OrganizationsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Organization.objects.all()
        return queryset
    
class OrganizationUsersAPIView(generics.ListAPIView):
    serializer_class = OrganizationUsersSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = OrganizationUser.objects.all()
        return queryset
    
class PositionsAPIView(generics.ListAPIView):
    serializer_class = PositionsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Position.objects.all()
        return queryset
    
class DepartmentsAPIView(generics.ListAPIView):
    serializer_class = DepartmentsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Department.objects.all()
        return queryset