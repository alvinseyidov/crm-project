from rest_framework import serializers

from accounting.models import *
from core.models import *
from django.contrib.auth import get_user_model
User = get_user_model()
from accounting.models import *


class TaxesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = "__all__"
