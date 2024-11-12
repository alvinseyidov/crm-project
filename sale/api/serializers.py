from rest_framework import serializers
from sale.models import SalesOrder, SalesOrderItem
from catalog.models import Product  # Assuming product model is in catalog app




# SalesOrderItem Serializer
class SalesOrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = SalesOrderItem
        fields = ['id', 'sales_order', 'product', 'product_name', 'quantity', 'price_per_unit', 'total_price',
                   'discount_percentage', 'tax_amount', 'tax']
        read_only_fields = ['total_price', 'tax_amount']


# SalesOrder Serializer
class SalesOrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    class Meta:
        model = SalesOrder
        fields = ['id', 'organization', 'customer', 'customer_name', 'order_number', 'date', 'delivery_date', 'status',
                  'description', 'total_amount', 'tax_amount', 'grand_total', 'created_at',
                  'updated_at']
        read_only_fields = ['order_number','total_amount', 'tax_amount', 'grand_total', 'created_at', 'updated_at']


