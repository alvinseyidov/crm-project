from django.urls import path
from .views import *

app_name = 'inventory-api'

urlpatterns = [
    path('warehouse/list/', WarehousesAPIView.as_view(), name ='warehouses'),
]