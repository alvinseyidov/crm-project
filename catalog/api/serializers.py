from rest_framework import serializers

from accounting.models import Tax
from catalog.models import (
    Category, Brand, ProductAttribute, ProductAttributeValue,
    Product, ProductImage, ProductCost, ProductPrice, Manufacturer
)


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'organization', 'name', 'logo', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ['id', 'organization', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'organization', 'name', 'parent', 'description', 'is_active']
        read_only_fields = ['id']

class ParentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'is_active']

# Category Serializer
class CategoryListSerializer(serializers.ModelSerializer):
    parent = ParentCategorySerializer(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'is_active']


class CategoryDetailSerializer(serializers.ModelSerializer):
    parent_name = serializers.CharField(source="parent.name", read_only=True)
    full_path = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'parent_name', 'description', 'image', 'is_active', 'created_at', 'updated_at', 'full_path']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_full_path(self, obj):
        """Recursively build the full path of categories."""
        return obj.get_full_path()


# Product Attribute Serializer
class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ['id', 'organization', 'name']
        read_only_fields = ['id']


# Product Attribute Value Serializer
class ProductAttributeValueSerializer(serializers.ModelSerializer):
    # Include the related attribute name for convenience in responses
    attribute_name = serializers.CharField(source="attribute.name", read_only=True)

    class Meta:
        model = ProductAttributeValue
        fields = ['id', 'attribute', 'attribute_name', 'value']
        read_only_fields = ['id']


class ProductTaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = "__all__"
        read_only_fields = ['id']


# Product Image Serializer
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"
        read_only_fields = ['id']


# Product Cost Serializer
class ProductCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCost
        fields = "__all__"
        read_only_fields = ['id']


# Product Price Serializer
class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = "__all__"
        read_only_fields = ['id']


# Product Serializer
class ProductListSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    manufacturer = ManufacturerSerializer(read_only=True)
    category = CategoryListSerializer(read_only=True)
    tax = ProductTaxSerializer(read_only=True)
    measurement_display = serializers.SerializerMethodField()
    type_display = serializers.SerializerMethodField()
    attributes = ProductAttributeValueSerializer(many=True, read_only=True)

    def get_measurement_display(self, obj):
        return obj.get_measurement_display()

    def get_type_display(self, obj):
        return obj.get_type_display()

    class Meta:
        model = Product
        fields = [
            'id', 'organization', 'category', 'name', 'sku', 'barcode', 'brand', 'type','manufacturer',
            'measurement', 'measurement_display', 'type_display', 'attributes', 'tax', 'description', 'is_active',
            'is_deleted','attributes',
            'created_at', 'updated_at', 'price', 'cost', 'stock'
        ]


class ProductCreateSerializer(serializers.ModelSerializer):
    attributes = serializers.PrimaryKeyRelatedField(
        queryset=ProductAttributeValue.objects.all(),
        many=True,
        required=False
    )
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ['id']


class ProductDetailSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    manufacturer = ManufacturerSerializer(read_only=True)
    category = CategoryDetailSerializer(read_only=True)
    tax = ProductTaxSerializer(read_only=True)
    attributes = ProductAttributeValueSerializer(many=True, read_only=True)


    class Meta:
        model = Product
        fields = [
            'id', 'organization',
            'category',
            'category_id', 'name', 'sku', 'barcode', 'brand',
            'measurement','manufacturer','attributes',
            'type',
            'tax',
            'tax_id',
            'description', 'is_active', 'is_deleted',
            'created_at', 'updated_at', 'price', 'cost', 'stock',
        ]
