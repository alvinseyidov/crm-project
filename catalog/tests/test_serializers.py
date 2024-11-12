# catalog/tests/test_serializers.py

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io
from catalog.api.serializers import *
from catalog.models import *
from organization.models import Organization
from rest_framework.exceptions import ValidationError
from datetime import date

@pytest.mark.django_db
class TestBrandSerializer:

    def test_valid_data(self):
        """Test BrandSerializer with valid data."""
        organization = Organization.objects.create(name="Test Organization")
        data = {
            "organization": organization.id,
            "name": "Test Brand",
            "description": "A test brand",
        }
        serializer = BrandSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        brand = serializer.save()
        assert brand.name == "Test Brand"
        assert brand.organization == organization

    def test_missing_name(self):
        """Test BrandSerializer without a name field."""
        organization = Organization.objects.create(name="Test Organization")
        data = {
            "organization": organization.id,
            "description": "A test brand",
        }
        serializer = BrandSerializer(data=data)
        assert not serializer.is_valid()
        assert "name" in serializer.errors


@pytest.mark.django_db
class TestManufacturerSerializer:

    def test_valid_data(self):
        """Test ManufacturerSerializer with valid data."""
        organization = Organization.objects.create(name="Test Organization")
        data = {
            "organization": organization.id,
            "name": "Test Manufacturer",
            "description": "A test manufacturer",
        }
        serializer = ManufacturerSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        manufacturer = serializer.save()
        assert manufacturer.name == "Test Manufacturer"
        assert manufacturer.organization == organization

    def test_missing_name(self):
        """Test ManufacturerSerializer without a name field."""
        organization = Organization.objects.create(name="Test Organization")
        data = {
            "organization": organization.id,
            "description": "A test manufacturer",
        }
        serializer = ManufacturerSerializer(data=data)
        assert not serializer.is_valid()
        assert "name" in serializer.errors



@pytest.mark.django_db
class TestProductAttributeSerializer:

    def test_valid_data(self):
        """Test ProductAttributeSerializer with valid data."""
        organization = Organization.objects.create(name="Test Organization")
        data = {
            "organization": organization.id,
            "name": "Color",
        }
        serializer = ProductAttributeSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        attribute = serializer.save()
        assert attribute.name == "Color"
        assert attribute.organization == organization

    def test_missing_name(self):
        """Test ProductAttributeSerializer without a name field."""
        organization = Organization.objects.create(name="Test Organization")
        data = {
            "organization": organization.id,
        }
        serializer = ProductAttributeSerializer(data=data)
        assert not serializer.is_valid()
        assert "name" in serializer.errors


@pytest.mark.django_db
class TestProductAttributeValueSerializer:

    def test_valid_data(self):
        """Test ProductAttributeValueSerializer with valid data."""
        organization = Organization.objects.create(name="Test Organization")
        attribute = ProductAttribute.objects.create(organization=organization, name="Color")
        data = {
            "attribute": attribute.id,
            "value": "Red",
        }
        serializer = ProductAttributeValueSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        attribute_value = serializer.save()
        assert attribute_value.value == "Red"
        assert attribute_value.attribute == attribute

    def test_missing_value(self):
        """Test ProductAttributeValueSerializer without a value field."""
        organization = Organization.objects.create(name="Test Organization")
        attribute = ProductAttribute.objects.create(organization=organization, name="Color")
        data = {
            "attribute": attribute.id,
        }
        serializer = ProductAttributeValueSerializer(data=data)
        assert not serializer.is_valid()
        assert "value" in serializer.errors



@pytest.mark.django_db
class TestCategorySerializers:

    def test_category_create_serializer_valid_data(self):
        """Test CategoryCreateSerializer with valid data."""
        organization = Organization.objects.create(name="Test Organization")
        data = {
            "organization": organization.id,
            "name": "Electronics",
            "is_active": True
        }
        serializer = CategoryCreateSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        category = serializer.save()
        assert category.name == "Electronics"
        assert category.organization == organization

    def test_category_list_serializer(self):
        """Test CategoryListSerializer fields."""
        organization = Organization.objects.create(name="Test Organization")
        parent_category = Category.objects.create(organization=organization, name="Parent Category")
        category = Category.objects.create(organization=organization, name="Child Category", parent=parent_category)

        serializer = CategoryListSerializer(category)
        data = serializer.data

        assert data["id"] == category.id
        assert data["name"] == "Child Category"
        assert data["parent"] == {
            "id": parent_category.id,
            "name": "Parent Category",
            "is_active": parent_category.is_active
        }

    def test_category_detail_serializer(self):
        """Test CategoryDetailSerializer fields."""
        organization = Organization.objects.create(name="Test Organization")
        parent_category = Category.objects.create(organization=organization, name="Parent Category")
        category = Category.objects.create(organization=organization, name="Child Category", parent=parent_category, description="A detailed description")

        serializer = CategoryDetailSerializer(category)
        data = serializer.data

        assert data["id"] == category.id
        assert data["name"] == "Child Category"
        assert data["parent"] == parent_category.id
        assert data["parent_name"] == "Parent Category"
        assert data["description"] == "A detailed description"
        assert "created_at" in data
        assert "updated_at" in data
        assert data["full_path"] == "Parent Category > Child Category"



@pytest.mark.django_db
class TestProductCreateSerializer:

    def test_valid_data(self, organization):
        """Test ProductCreateSerializer with valid data."""
        data = {
            "organization": organization.id,
            "name": "New Product",
            "sku": "SKU123",
            "type": "product",
            "is_active": True,
            "attributes": []
        }
        serializer = ProductCreateSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        product = serializer.save()
        assert product.name == "New Product"
        assert product.sku == "SKU123"
        assert product.type == "product"

    def test_valid_agriculture_data(self, organization):
        """Test ProductCreateSerializer with valid data for agriculture product type."""
        data = {
            "organization": organization.id,
            "name": "Agriculture Product",
            "sku": "SKU124",
            "type": "agriculture",
            "is_active": True,
            "attributes": []
        }
        serializer = ProductCreateSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        product = serializer.save()
        assert product.name == "Agriculture Product"
        assert product.type == "agriculture"

    def test_missing_required_field(self, organization):
        """Test ProductCreateSerializer with missing required fields."""
        data = {"organization": organization.id, "sku": "SKU123"}
        serializer = ProductCreateSerializer(data=data)
        assert not serializer.is_valid()
        assert "name" in serializer.errors

    def test_invalid_attributes(self, organization):
        """Test ProductCreateSerializer with invalid attribute IDs."""
        data = {
            "organization": organization.id,
            "name": "Product with Invalid Attributes",
            "sku": "SKU456",
            "type": "product",
            "attributes": [999]  # Non-existent attribute ID
        }
        serializer = ProductCreateSerializer(data=data)
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
class TestProductListSerializer:

    def test_product_list_output(self, product, attribute):
        """Test ProductListSerializer output format."""
        product.attributes.add(attribute)
        serializer = ProductListSerializer(product)

        # Check basic fields
        assert serializer.data["name"] == product.name
        assert serializer.data["sku"] == product.sku

        # Check product type field
        assert serializer.data["type"] == product.type

        # Check custom display fields
        assert "measurement_display" in serializer.data
        assert "type_display" in serializer.data

        # Check attributes formatting
        assert serializer.data["attributes"][0]["id"] == attribute.id
        assert serializer.data["attributes"][0]["attribute_name"] == attribute.attribute.name


@pytest.mark.django_db
class TestProductDetailSerializer:

    def test_product_detail_output(self, product, attribute):
        """Test ProductDetailSerializer output format."""
        product.attributes.add(attribute)
        serializer = ProductDetailSerializer(product)

        # Check main fields
        assert serializer.data["name"] == product.name
        assert serializer.data["sku"] == product.sku

        # Check product type
        assert serializer.data["type"] == product.type

        # Verify nested serializers
        assert "brand" in serializer.data
        assert "category" in serializer.data

        # Check attributes in detail view
        assert "attributes" in serializer.data
        assert serializer.data["attributes"][0]["id"] == attribute.id
        assert serializer.data["attributes"][0]["attribute_name"] == attribute.attribute.name


@pytest.mark.django_db
class TestProductImageSerializer:

    def test_product_image_serializer(self, product):
        """Test ProductImageSerializer with valid data, including a real test image."""
        # Generate a simple in-memory image file
        image = Image.new('RGB', (100, 100), color='red')
        image_file = io.BytesIO()
        image.save(image_file, format='JPEG')
        image_file.seek(0)  # Reset file pointer to the beginning

        test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=image_file.read(),
            content_type='image/jpeg'
        )

        data = {"product": product.id, "sorting": 1, "image": test_image}
        serializer = ProductImageSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        image_instance = serializer.save()
        assert image_instance.product == product
        assert image_instance.sorting == 1


@pytest.mark.django_db
class TestProductCostSerializer:

    def test_product_cost_serializer(self, product, vendor):
        """Test ProductCostSerializer with valid data."""
        data = {
            "product": product.id,
            "amount": "100.00",
            "date": date.today(),
            "vendor": vendor.id
        }
        serializer = ProductCostSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        cost = serializer.save()
        assert cost.product == product
        assert cost.amount == 100.00
        assert cost.vendor == vendor


@pytest.mark.django_db
class TestProductPriceSerializer:

    def test_product_price_serializer(self, product):
        """Test ProductPriceSerializer with valid data."""
        data = {
            "product": product.id,
            "amount": "150.00",
            "date": date.today()
        }
        serializer = ProductPriceSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        price = serializer.save()
        assert price.product == product
        assert price.amount == 150.00
