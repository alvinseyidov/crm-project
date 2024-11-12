from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accounting.api.serializers import *

class TaxesAPIView(generics.ListAPIView):
    serializer_class = TaxesSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # queryset = Tax.objects.filter(organization=self.request.user.organization)
        queryset = Tax.objects.filter(organization__id=self.request.query_params.get('org_id'))
        return queryset

     