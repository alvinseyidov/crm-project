from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from inventory.api.serializers import *
from inventory.models import *

class WarehousesAPIView(generics.ListAPIView):
    serializer_class = WareHousesSerialize
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Warehouse.objects.all()
        return queryset