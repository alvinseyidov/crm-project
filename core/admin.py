from django.contrib import admin
from .models import *

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['country','name']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['city','lat','lon','postcode','line1','line2']


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ['ext','phone','type']


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['name','symbol']


@admin.register(CurrencyRate)
class CurrencyRateAdmin(admin.ModelAdmin):
    list_display = ['organization','from_currency','to_currency','rate','date','created_at','updated_at']