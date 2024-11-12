from rest_framework import serializers

from auth.models import *
from core.models import *
from django.contrib.auth import get_user_model

from organization.models import Organization, OrganizationUser

User = get_user_model()
from auth.models import *

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"

class OrganizationUserSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()
    class Meta:
        model = OrganizationUser
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    organizations = OrganizationUserSerializer(many=True)
    class Meta:
        model = User
        fields = "__all__"