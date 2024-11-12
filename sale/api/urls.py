from django.urls import path
from .views import (
    SalesOrderListCreateView,
    SalesOrderRetrieveUpdateDestroyView,
    SalesOrderItemListCreateView
)
app_name = 'sale-api'
urlpatterns = [
    # SalesOrder endpoints
    path('sales-orders/', SalesOrderListCreateView.as_view(), name='salesorder-list-create'),
    path('sales-orders/<int:pk>/', SalesOrderRetrieveUpdateDestroyView.as_view(), name='salesorder-detail'),

    # SalesOrderItem endpoints (Optional)
    path('sales-order-items/', SalesOrderItemListCreateView.as_view(), name='salesorderitem-list-create'),
]
