# catalog/tests/test_models.py
import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from catalog.models import *
from organization.models import Organization
from catalog.models import Product, ProductImage, ProductCost, ProductPrice
from catalog.models import Category, Brand, Manufacturer, ProductAttributeValue
from accounting.models import Tax
from purchase.models import Vendor


@pytest.mark.django_db
class TestManufacturerModel:

    def test_create_manufacturer(self):
        """Test creating a Manufacturer with basic fields."""
        organization = Organization.objects.create(name="Test Organization")
        manufacturer = Manufacturer.objects.create(
            organization=organization,
            name="Test Manufacturer",
            description="This is a test manufacturer."
        )
        assert manufacturer.name == "Test Manufacturer"
        assert manufacturer.organization == organization

    def test_unique_manufacturer_name_per_organization(self):
        """Test that Manufacturer names are unique within an organization."""
        organization = Organization.objects.create(name="Test Organization")
        Manufacturer.objects.create(organization=organization, name="Test Manufacturer")
        with pytest.raises(Exception):  # Should raise IntegrityError or ValidationError
            duplicate_manufacturer = Manufacturer(organization=organization, name="Test Manufacturer")
            duplicate_manufacturer.full_clean()  # Triggers validation for unique constraint

    def test_manufacturer_str(self):
        """Test the string representation of the Manufacturer model."""
        organization = Organization.objects.create(name="Test Organization")
        manufacturer = Manufacturer.objects.create(organization=organization, name="Test Manufacturer")
        assert str(manufacturer) == "Test Organization - Test Manufacturer"

    def test_manufacturer_display_name(self):
        """Test get_display_name method for Manufacturer."""
        organization = Organization.objects.create(name="Test Organization")
        manufacturer = Manufacturer.objects.create(organization=organization, name="Test Manufacturer")
        assert manufacturer.get_display_name() == "Test Organization - Test Manufacturer"
        assert manufacturer.get_display_name(show_organization=False) == "Test Manufacturer"


@pytest.mark.django_db
class TestBrandModel:

    def test_create_brand(self):
        """Test creating a Brand with basic fields."""
        organization = Organization.objects.create(name="Test Organization")
        brand = Brand.objects.create(
            organization=organization,
            name="Test Brand",
            description="This is a test brand."
        )
        assert brand.name == "Test Brand"
        assert brand.organization == organization

    def test_unique_brand_name_per_organization(self):
        """Test that Brand names are unique within an organization."""
        organization = Organization.objects.create(name="Test Organization")
        Brand.objects.create(organization=organization, name="Test Brand")
        with pytest.raises(Exception):  # Should raise IntegrityError or ValidationError
            duplicate_brand = Brand(organization=organization, name="Test Brand")
            duplicate_brand.full_clean()  # Triggers validation for unique constraint

    def test_brand_str(self):
        """Test the string representation of the Brand model."""
        organization = Organization.objects.create(name="Test Organization")
        brand = Brand.objects.create(organization=organization, name="Test Brand")
        assert str(brand) == "Test Organization - Test Brand"

    def test_brand_display_name(self):
        """Test get_display_name method for Brand."""
        organization = Organization.objects.create(name="Test Organization")
        brand = Brand.objects.create(organization=organization, name="Test Brand")
        assert brand.get_display_name() == "Test Organization - Test Brand"
        assert brand.get_display_name(show_organization=False) == "Test Brand"


@pytest.mark.django_db
class TestCategoryModel:

    def test_create_category(self):
        """Test creating a category and basic field values."""
        organization = Organization.objects.create(name="Test Organization")
        category = Category.objects.create(
            organization=organization,
            name="Electronics"
        )
        assert category.name == "Electronics"
        assert category.organization == organization

    def test_unique_category_name_per_organization(self):
        """Test that category names are unique within an organization."""
        organization = Organization.objects.create(name="Test Organization")
        Category.objects.create(organization=organization, name="Electronics")
        with pytest.raises(ValidationError):
            duplicate_category = Category(organization=organization, name="Electronics")
            duplicate_category.full_clean()  # Triggers validation

    def test_get_full_path(self):
        """Test that get_full_path returns the correct hierarchical path."""
        organization = Organization.objects.create(name="Test Organization")
        parent_category = Category.objects.create(organization=organization, name="Electronics")
        sub_category = Category.objects.create(organization=organization, name="Phones", parent=parent_category)
        assert sub_category.get_full_path() == "Electronics > Phones"

    def test_get_ancestors(self):
        """Test that get_ancestors returns all parent categories in correct order."""
        organization = Organization.objects.create(name="Test Organization")
        parent_category = Category.objects.create(organization=organization, name="Electronics")
        child_category = Category.objects.create(organization=organization, name="Phones", parent=parent_category)
        grandchild_category = Category.objects.create(organization=organization, name="Smartphones",
                                                      parent=child_category)

        ancestors = grandchild_category.get_ancestors()
        assert list(ancestors) == [parent_category, child_category]

    def test_image_validation(self):
        """Test that an oversized image raises a ValidationError (if image validation is set up)."""
        organization = Organization.objects.create(name="Test Organization")
        large_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'a' * (2 * 1024 * 1024 + 1),  # 2 MB + 1 byte
            content_type='image/jpeg'
        )

        category = Category(
            organization=organization,
            name="Oversized Image Category",
            image=large_image
        )

        # This should raise a ValidationError due to image size
        with pytest.raises(ValidationError):
            category.full_clean()  # This triggers validation

@pytest.mark.django_db
class TestProductAttributeModel:

    def test_create_product_attribute(self):
        """Test creating a ProductAttribute with essential fields."""
        organization = Organization.objects.create(name="Test Organization")
        attribute = ProductAttribute.objects.create(
            organization=organization,
            name="Color"
        )
        assert attribute.name == "Color"
        assert attribute.organization == organization

    def test_unique_product_attribute_name_per_organization(self):
        """Test that ProductAttribute names are unique within an organization."""
        organization = Organization.objects.create(name="Test Organization")
        ProductAttribute.objects.create(organization=organization, name="Color")
        with pytest.raises(Exception):  # Should raise IntegrityError or ValidationError
            duplicate_attribute = ProductAttribute(organization=organization, name="Color")
            duplicate_attribute.full_clean()  # Triggers validation for unique constraint

    def test_product_attribute_str(self):
        """Test the string representation of the ProductAttribute model."""
        organization = Organization.objects.create(name="Test Organization")
        attribute = ProductAttribute.objects.create(organization=organization, name="Size")
        assert str(attribute) == "Size"


@pytest.mark.django_db
class TestProductAttributeValueModel:

    def test_create_product_attribute_value(self):
        """Test creating a ProductAttributeValue with essential fields."""
        organization = Organization.objects.create(name="Test Organization")
        attribute = ProductAttribute.objects.create(organization=organization, name="Color")
        value = ProductAttributeValue.objects.create(attribute=attribute, value="Red")
        assert value.value == "Red"
        assert value.attribute == attribute

    def test_unique_product_attribute_value_per_attribute(self):
        """Test that ProductAttributeValue values are unique per attribute."""
        organization = Organization.objects.create(name="Test Organization")
        attribute = ProductAttribute.objects.create(organization=organization, name="Color")
        ProductAttributeValue.objects.create(attribute=attribute, value="Red")
        with pytest.raises(Exception):  # Should raise IntegrityError or ValidationError
            duplicate_value = ProductAttributeValue(attribute=attribute, value="Red")
            duplicate_value.full_clean()  # Triggers validation for unique constraint

    def test_product_attribute_value_str(self):
        """Test the string representation of the ProductAttributeValue model."""
        organization = Organization.objects.create(name="Test Organization")
        attribute = ProductAttribute.objects.create(organization=organization, name="Material")
        value = ProductAttributeValue.objects.create(attribute=attribute, value="Cotton")
        assert str(value) == "Material: Cotton"

    def test_organization_property(self):
        """Test that organization property of ProductAttributeValue returns correct organization."""
        organization = Organization.objects.create(name="Test Organization")
        attribute = ProductAttribute.objects.create(organization=organization, name="Size")
        value = ProductAttributeValue.objects.create(attribute=attribute, value="Large")
        assert value.organization == organization


@pytest.mark.django_db
class TestProductModel:

    def test_create_product(self):
        """Test creating a Product with basic fields."""
        organization = Organization.objects.create(name="Test Organization")
        category = Category.objects.create(organization=organization, name="Electronics")
        tax = Tax.objects.create(organization=organization, name="Standard", percent=18)
        product = Product.objects.create(
            organization=organization,
            category=category,
            name="Test Product",
            sku="SKU123",
            barcode="BARCODE123",
            tax=tax,
            measurement="pc",
            type="product"
        )
        assert product.name == "Test Product"
        assert product.organization == organization
        assert product.category == category

    def test_unique_sku_and_barcode_per_organization(self):
        """Test that SKU and barcode are unique within an organization."""
        organization = Organization.objects.create(name="Test Organization")
        Product.objects.create(organization=organization, name="Test Product", sku="SKU123", barcode="BARCODE123")
        with pytest.raises(Exception):
            duplicate_product = Product(organization=organization, name="Duplicate Product", sku="SKU123")
            duplicate_product.full_clean()  # Triggers validation for unique constraint

    def test_product_get_first_image(self, rf):
        """Test get_first_image method."""
        request = rf.get('/')  # Using Django's RequestFactory for a mock request
        organization = Organization.objects.create(name="Test Organization")
        product = Product.objects.create(organization=organization, name="Test Product")
        ProductImage.objects.create(product=product, image="path/to/image.jpg")

        image_url = product.get_first_image(request)
        assert image_url.endswith("path/to/image.jpg")

    def test_product_cost_property(self):
        """Test cost property to retrieve the latest product cost."""
        organization = Organization.objects.create(name="Test Organization")
        product = Product.objects.create(organization=organization, name="Test Product")
        ProductCost.objects.create(product=product, amount=100, date="2023-01-01")
        ProductCost.objects.create(product=product, amount=200, date="2023-02-01")

        assert product.cost == 200  # Should retrieve the latest cost

    def test_product_price_property(self):
        """Test price property to retrieve the latest product price."""
        organization = Organization.objects.create(name="Test Organization")
        product = Product.objects.create(organization=organization, name="Test Product")
        ProductPrice.objects.create(product=product, amount=150, date="2023-01-01")
        ProductPrice.objects.create(product=product, amount=250, date="2023-02-01")

        assert product.price == 250  # Should retrieve the latest price

    def test_default_tax_category(self):
        """Test default tax and category assignment in save method."""
        organization = Organization.objects.create(name="Test Organization")
        product = Product.objects.create(
            organization=organization,
            name="Test Product",
            sku="SKU123"
        )
        assert product.tax.percent == 0  # Default tax percent is 0
        assert product.category.name == "Uncategorized"

    def test_is_trade_margin(self, organization):
        """Test that agriculture products are recognized as trade margin."""
        product = Product.objects.create(
            name="Agriculture Item",
            sku="SKU789",
            organization=organization,
            type="agriculture",
            is_active=True
        )
        assert product.is_trade_margin() is True

        # Test with a standard product to confirm `is_trade_margin` returns False
        non_trade_margin_product = Product.objects.create(
            name="Standard Product",
            sku="SKU456",
            organization=organization,
            type="product",
            is_active=True
        )
        assert non_trade_margin_product.is_trade_margin() is False


@pytest.mark.django_db
class TestProductImageModel:

    def test_product_image_creation(self):
        """Test creating a ProductImage with basic fields."""
        organization = Organization.objects.create(name="Test Organization")
        product = Product.objects.create(organization=organization, name="Test Product")
        product_image = ProductImage.objects.create(product=product, image="path/to/image.jpg", sorting=1)

        assert product_image.product == product
        assert product_image.sorting == 1

    def test_product_image_sorting_order(self):
        """Test that ProductImages are ordered by sorting field."""
        organization = Organization.objects.create(name="Test Organization")
        product = Product.objects.create(organization=organization, name="Test Product")
        img1 = ProductImage.objects.create(product=product, image="img1.jpg", sorting=2)
        img2 = ProductImage.objects.create(product=product, image="img2.jpg", sorting=1)

        images = list(product.images.all())
        assert images == [img2, img1]  # Sorted by sorting field


@pytest.mark.django_db
class TestProductCostModel:

    def test_product_cost_creation(self):
        """Test creating a ProductCost with essential fields."""
        organization = Organization.objects.create(name="Test Organization")
        product = Product.objects.create(organization=organization, name="Test Product")
        vendor = Vendor.objects.create(organization=organization,name="Test Vendor")
        cost = ProductCost.objects.create(product=product, amount=100, date="2023-01-01", vendor=vendor)

        assert cost.product == product
        assert cost.amount == 100
        assert cost.vendor == vendor

    def test_product_cost_ordering(self):
        """Test that ProductCosts are ordered by date and ID descending."""
        organization = Organization.objects.create(name="Test Organization")
        product = Product.objects.create(organization=organization, name="Test Product")
        cost1 = ProductCost.objects.create(product=product, amount=100, date="2023-01-01")
        cost2 = ProductCost.objects.create(product=product, amount=200, date="2023-02-01")

        costs = list(product.costs.all())
        assert costs == [cost2, cost1]  # Ordered by date descending


@pytest.mark.django_db
class TestProductPriceModel:

    def test_product_price_creation(self):
        """Test creating a ProductPrice with essential fields."""
        organization = Organization.objects.create(name="Test Organization")
        product = Product.objects.create(organization=organization, name="Test Product")
        price = ProductPrice.objects.create(product=product, amount=150, date="2023-01-01")

        assert price.product == product
        assert price.amount == 150

    def test_product_price_ordering(self):
        """Test that ProductPrices are ordered by date and ID descending."""
        organization = Organization.objects.create(name="Test Organization")
        product = Product.objects.create(organization=organization, name="Test Product")
        price1 = ProductPrice.objects.create(product=product, amount=100, date="2023-01-01")
        price2 = ProductPrice.objects.create(product=product, amount=200, date="2023-02-01")

        prices = list(product.prices.all())
        assert prices == [price2, price1]  # Ordered by date descending
