from django.urls import path
from .views import *
from accounting.api import views as api_views

app_name = 'accounting-api'

urlpatterns = [
    path('tax/list/', TaxesAPIView.as_view(), name ='taxes'),
]