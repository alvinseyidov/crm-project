from rest_framework import serializers

from inventory.models import *
from core.models import *
from django.contrib.auth import get_user_model
User = get_user_model()

class WareHousesSerialize(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = "__all__"