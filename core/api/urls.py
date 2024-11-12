from django.urls import path
from .views import *
from core.api import views as api_views

app_name = 'core-api'

urlpatterns = [
    path('country/list/',api_views.CountriesAPIView.as_view(), name ='countries'),
    path('city/list/',api_views.CitiesAPIView.as_view(), name ='cities'),
    path('address/list/',api_views.AddressesAPIView.as_view(), name ='addresses'),
    path('phone/list/',api_views.PhonesAPIView.as_view(), name ='phones'),
    path('currency/list/',api_views.CurrenciesAPIView.as_view(), name ='currencies'),
    path('currencyrate/list/',api_views.CurrencyRatesAPIView.as_view(), name ='currencyrates'),
]