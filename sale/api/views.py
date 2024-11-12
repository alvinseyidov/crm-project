from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from sale.models import SalesOrder, SalesOrderItem
from .serializers import SalesOrderSerializer, SalesOrderItemSerializer


# SalesOrder Views
class SalesOrderListCreateView(generics.ListCreateAPIView):
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Optionally filter by organization or status via query param.
        """
        queryset = super().get_queryset()
        org_id = self.request.query_params.get('org_id')
        status = self.request.query_params.get('status')
        if org_id:
            queryset = queryset.filter(organization__id=org_id)
        if status:
            queryset = queryset.filter(status=status)
        return queryset

class SalesOrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

# SalesOrderItem Views (Optional)
class SalesOrderItemListCreateView(generics.ListCreateAPIView):
    queryset = SalesOrderItem.objects.all()
    serializer_class = SalesOrderItemSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Optionally filter by sales_order_id via query param.
        """
        queryset = super().get_queryset()
        sales_order_id = self.request.query_params.get('sales_order_id')
        if sales_order_id:
            queryset = queryset.filter(sales_order__id=sales_order_id)
        return queryset
