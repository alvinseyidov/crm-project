from rest_framework import serializers

from organization.models import *
from core.models import *
from django.contrib.auth import get_user_model
User = get_user_model()
from organization.models import *


class OrganizationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"

class OrganizationUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationUser
        fields = "__all__"

class PositionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = "__all__"

class DepartmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"