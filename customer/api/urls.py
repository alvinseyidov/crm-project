from django.urls import path
from .views import (
    CustomerListCreateView,
    CustomerRetrieveUpdateDestroyView,
)
app_name = 'customer-api'
urlpatterns = [
    # Customer endpoints
    path('customers/', CustomerListCreateView.as_view(), name='customer-list-create'),
    path('customers/<int:pk>/', CustomerRetrieveUpdateDestroyView.as_view(), name='customer-detail'),
    ]