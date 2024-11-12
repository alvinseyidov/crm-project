from rest_framework import serializers

from core.models import Country
from purchase.models import Vendor, Purchase, PurchaseItem, LandedCost, PurchaseReceive, PurchaseReceiveItem, \
    PurchaseDocument
from rest_framework import serializers


# Vendor Serializer
class VendorSerializer(serializers.ModelSerializer):
    country = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Vendor
        fields = [
            'id', 'organization', 'name', 'email', 'phone', 'address',
            'country', 'tin', 'contact_person', 'description', 'logo_image',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']



class LandedCostSerializer(serializers.ModelSerializer):
    purchase_order_number = serializers.CharField(source="purchase.order_number", read_only=True)
    class Meta:
        model = LandedCost
        fields = [
            'id',
            'organization',
            'purchase',
            'purchase_order_number',
            'cost_type',
            'amount',
            'description',
            'document',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']



class PurchaseDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseDocument
        fields = ['id', 'purchase', 'document', 'description', 'uploaded_at']



class PurchaseItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    tax_display = serializers.CharField(source="tax.name", read_only=True)
    tax_percent = serializers.CharField(source="tax.percent", read_only=True)

    class Meta:
        model = PurchaseItem
        fields = [
            'id', 'purchase', 'product', 'product_name', 'quantity', 'unit_cost', 'item_total_cost',
            'tax_amount', 'discount_amount', 'allocated_landed_cost', 'grand_total', 'weight',
            'volume', 'tax', 'tax_display', 'tax_percent','created_at', 'updated_at'
        ]
        read_only_fields = ['item_total_cost', 'grand_total', 'tax_amount', 'product_name', 'tax_display','tax_percent']


class PurchaseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = [
            'id','organization', 'vendor', 'order_number', 'customs_reference_number', 'customs_payment_term',
            'currency', 'currency_rate', 'purchase_origin', 'allocation_method', 'date', 'expected_delivery_date',
            'status', 'total_amount', 'tax_amount', 'grand_total', 'description'
        ]
        read_only_fields = ['id',]


class PurchaseListSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    purchase_origin_display = serializers.CharField(source='get_purchase_origin_display', read_only=True)
    allocation_method_display = serializers.CharField(source='get_allocation_method_display', read_only=True)

    class Meta:
        model = Purchase
        fields = [
            'id', 'order_number', 'date', 'status',
            'total_amount', 'grand_total', 'currency','vendor',
            'status_display',
            'purchase_origin_display',
            'allocation_method_display',
        ]


class PurchaseDetailSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer()
    items = PurchaseItemSerializer(many=True, read_only=True)
    landed_costs = LandedCostSerializer(many=True, read_only=True)
    documents = PurchaseDocumentSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    purchase_origin_display = serializers.CharField(source='get_purchase_origin_display', read_only=True)
    allocation_method_display = serializers.CharField(source='get_allocation_method_display', read_only=True)
    class Meta:
        model = Purchase
        fields = [
            'id', 'vendor', 'order_number', 'customs_reference_number','documents',
            'customs_payment_term', 'currency', 'currency_rate', 'purchase_origin', 'allocation_method',
            'date', 'expected_delivery_date', 'status', 'total_amount',
            'tax_amount', 'grand_total', 'description', 'created_at', 'updated_at','items','landed_costs',
            'status_display',

            'purchase_origin_display',
            'allocation_method_display',
        ]




class PurchaseReceiveItemDetailSerializer(serializers.ModelSerializer):
    """Detailed Serializer for PurchaseReceiveItem model, includes product details."""
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = PurchaseReceiveItem
        fields = [
            'id', 'purchase_receive','product_name', 'product', 'ordered_quantity',
            'received_quantity', 'is_fully_received'
        ]
        read_only_fields = ['is_fully_received']


class PurchaseReceiveDetailSerializer(serializers.ModelSerializer):
    """Detailed Serializer for PurchaseReceive model, includes all item details."""

    receive_items = PurchaseReceiveItemDetailSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = PurchaseReceive
        fields = [
            'id', 'purchase', 'organization', 'receive_date', 'status', 'status_display',
            'total_received_quantity', 'remarks', 'created_at', 'updated_at', 'receive_items'
        ]
        read_only_fields = ['receive_date', 'total_received_quantity', 'created_at', 'updated_at']



class PurchaseReceiveItemSerializer(serializers.ModelSerializer):
    """Serializer for PurchaseReceiveItem model, includes validation for received quantity."""

    class Meta:
        model = PurchaseReceiveItem
        fields = ['id', 'purchase_receive', 'product', 'ordered_quantity', 'received_quantity', 'is_fully_received']
        read_only_fields = ['is_fully_received']

    def validate_received_quantity(self, value):
        """Ensure that received quantity does not exceed ordered quantity."""
        # Only perform the validation if self.instance exists (i.e., during updates)
        if self.instance and value > self.instance.ordered_quantity:
            raise serializers.ValidationError("Received quantity cannot exceed ordered quantity.")
        return value

class PurchaseReceiveSerializer(serializers.ModelSerializer):
    """Serializer for PurchaseReceive model, includes related receive items."""

    receive_items = PurchaseReceiveItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = PurchaseReceive
        fields = [
            'id', 'purchase', 'organization', 'receive_date', 'status', 'status_display',
            'total_received_quantity', 'remarks', 'created_at', 'updated_at', 'receive_items'
        ]
        read_only_fields = ['receive_date', 'total_received_quantity', 'created_at', 'updated_at']

    def update(self, instance, validated_data):
        """Custom update method to handle total received quantity recalculation."""
        instance = super().update(instance, validated_data)
        instance.update_received_quantity()  # Update the total received quantity based on related items
        return instance





