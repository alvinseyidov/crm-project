from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from core.models import *

User = get_user_model()

class CountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"

class CitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"

class AddressesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"

class PhonesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = "__all__"

class CurrenciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = "__all__"

class CurrencyRatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyRate
        fields = "__all__"