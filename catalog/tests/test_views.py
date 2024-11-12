# catalog/tests/test_views.py

import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status


from catalog.models import *
from organization.models import Organization




@pytest.mark.django_db
class TestBrandViews:

    def test_list_brands(self, api_client, organization):
        """Test listing brands with organization filter."""
        Brand.objects.create(organization=organization, name="Brand 1")
        Brand.objects.create(organization=organization, name="Brand 2")

        # Make an authenticated GET request with the organization filter
        response = api_client.get(f"/api/catalog/brands/?org_id={organization.id}")

        # Validate response
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_create_brand(self, api_client, organization):
        """Test creating a brand with valid data."""
        data = {
            "organization": organization.id,
            "name": "New Brand",
            "description": "Brand description",
        }
        response = api_client.post("/api/catalog/brands/", data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Brand.objects.filter(name="New Brand").exists()

    def test_retrieve_brand(self, api_client, organization):
        """Test retrieving a specific brand."""
        brand = Brand.objects.create(organization=organization, name="Brand 1")
        response = api_client.get(f"/api/catalog/brands/{brand.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == brand.name

    def test_update_brand(self, api_client, organization):
        """Test updating a specific brand."""
        brand = Brand.objects.create(organization=organization, name="Old Brand")
        data = {"name": "Updated Brand"}
        response = api_client.patch(f"/api/catalog/brands/{brand.id}/", data)
        assert response.status_code == status.HTTP_200_OK
        brand.refresh_from_db()
        assert brand.name == "Updated Brand"

    def test_delete_brand(self, api_client, organization):
        """Test deleting a specific brand."""
        brand = Brand.objects.create(organization=organization, name="Brand to Delete")
        response = api_client.delete(f"/api/catalog/brands/{brand.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Brand.objects.filter(name="Brand to Delete").exists()


@pytest.mark.django_db
class TestManufacturerViews:

    def test_list_manufacturers(self, api_client, organization):
        """Test listing manufacturers with organization filter."""
        Manufacturer.objects.create(organization=organization, name="Manufacturer 1")
        Manufacturer.objects.create(organization=organization, name="Manufacturer 2")

        # Make an authenticated GET request with the organization filter
        response = api_client.get(f"/api/catalog/manufacturers/?org_id={organization.id}")

        # Validate response
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_create_manufacturer(self, api_client, organization):
        """Test creating a manufacturer with valid data."""
        data = {
            "organization": organization.id,
            "name": "New Manufacturer",
            "description": "Manufacturer description",
        }
        response = api_client.post("/api/catalog/manufacturers/", data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Manufacturer.objects.filter(name="New Manufacturer").exists()

    def test_retrieve_manufacturer(self, api_client, organization):
        """Test retrieving a specific manufacturer."""
        manufacturer = Manufacturer.objects.create(organization=organization, name="Manufacturer 1")
        response = api_client.get(f"/api/catalog/manufacturers/{manufacturer.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == manufacturer.name

    def test_update_manufacturer(self, api_client, organization):
        """Test updating a specific manufacturer."""
        manufacturer = Manufacturer.objects.create(organization=organization, name="Old Manufacturer")
        data = {"name": "Updated Manufacturer"}
        response = api_client.patch(f"/api/catalog/manufacturers/{manufacturer.id}/", data)
        assert response.status_code == status.HTTP_200_OK
        manufacturer.refresh_from_db()
        assert manufacturer.name == "Updated Manufacturer"

    def test_delete_manufacturer(self, api_client, organization):
        """Test deleting a specific manufacturer."""
        manufacturer = Manufacturer.objects.create(organization=organization, name="Manufacturer to Delete")
        response = api_client.delete(f"/api/catalog/manufacturers/{manufacturer.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Manufacturer.objects.filter(name="Manufacturer to Delete").exists()


@pytest.mark.django_db
class TestProductAttributeViews:

    def test_list_product_attributes(self, api_client, organization):
        """Test listing product attributes with organization filter."""
        ProductAttribute.objects.create(organization=organization, name="Color")
        ProductAttribute.objects.create(organization=organization, name="Size")

        response = api_client.get(f"/api/catalog/attributes/?org_id={organization.id}")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_create_product_attribute(self, api_client, organization):
        """Test creating a product attribute with valid data."""
        data = {
            "organization": organization.id,
            "name": "Material",
        }
        response = api_client.post("/api/catalog/attributes/", data)
        assert response.status_code == status.HTTP_201_CREATED
        assert ProductAttribute.objects.filter(name="Material").exists()

    def test_retrieve_product_attribute(self, api_client, organization):
        """Test retrieving a specific product attribute."""
        attribute = ProductAttribute.objects.create(organization=organization, name="Size")
        response = api_client.get(f"/api/catalog/attributes/{attribute.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == attribute.name

    def test_update_product_attribute(self, api_client, organization):
        """Test updating a specific product attribute."""
        attribute = ProductAttribute.objects.create(organization=organization, name="Old Name")
        data = {"name": "Updated Name"}
        response = api_client.patch(f"/api/catalog/attributes/{attribute.id}/", data)
        assert response.status_code == status.HTTP_200_OK
        attribute.refresh_from_db()
        assert attribute.name == "Updated Name"

    def test_delete_product_attribute(self, api_client, organization):
        """Test deleting a specific product attribute."""
        attribute = ProductAttribute.objects.create(organization=organization, name="To Delete")
        response = api_client.delete(f"/api/catalog/attributes/{attribute.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not ProductAttribute.objects.filter(name="To Delete").exists()


@pytest.mark.django_db
class TestProductAttributeValueViews:

    def test_list_product_attribute_values(self, api_client, organization):
        """Test listing product attribute values with organization filter."""
        attribute = ProductAttribute.objects.create(organization=organization, name="Color")
        ProductAttributeValue.objects.create(attribute=attribute, value="Red")
        ProductAttributeValue.objects.create(attribute=attribute, value="Blue")

        response = api_client.get(f"/api/catalog/attribute-values/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_create_product_attribute_value(self, api_client, organization):
        """Test creating a product attribute value with valid data."""
        attribute = ProductAttribute.objects.create(organization=organization, name="Material")
        data = {
            "attribute": attribute.id,
            "value": "Cotton",
        }
        response = api_client.post("/api/catalog/attribute-values/", data)
        assert response.status_code == status.HTTP_201_CREATED
        assert ProductAttributeValue.objects.filter(value="Cotton").exists()

    def test_retrieve_product_attribute_value(self, api_client, organization):
        """Test retrieving a specific product attribute value."""
        attribute = ProductAttribute.objects.create(organization=organization, name="Size")
        attribute_value = ProductAttributeValue.objects.create(attribute=attribute, value="Large")

        response = api_client.get(f"/api/catalog/attribute-values/{attribute_value.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["value"] == attribute_value.value

    def test_update_product_attribute_value(self, api_client, organization):
        """Test updating a specific product attribute value."""
        attribute = ProductAttribute.objects.create(organization=organization, name="Size")
        attribute_value = ProductAttributeValue.objects.create(attribute=attribute, value="Small")
        data = {"value": "Medium"}

        response = api_client.patch(f"/api/catalog/attribute-values/{attribute_value.id}/", data)
        assert response.status_code == status.HTTP_200_OK
        attribute_value.refresh_from_db()
        assert attribute_value.value == "Medium"

    def test_delete_product_attribute_value(self, api_client, organization):
        """Test deleting a specific product attribute value."""
        attribute = ProductAttribute.objects.create(organization=organization, name="Color")
        attribute_value = ProductAttributeValue.objects.create(attribute=attribute, value="Green")

        response = api_client.delete(f"/api/catalog/attribute-values/{attribute_value.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not ProductAttributeValue.objects.filter(value="Green").exists()


@pytest.mark.django_db
class TestCategoryViews:

    def test_list_categories(self, api_client, organization):
        """Test listing categories with organization filter."""
        Category.objects.create(organization=organization, name="Electronics")
        Category.objects.create(organization=organization, name="Clothing")

        response = api_client.get(f"/api/catalog/categories/?org_id={organization.id}")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_create_category(self, api_client, organization):
        """Test creating a category with valid data."""
        data = {
            "organization": organization.id,
            "name": "Home Appliances",
            "is_active": True
        }
        response = api_client.post("/api/catalog/categories/create/", data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Category.objects.filter(name="Home Appliances").exists()

    def test_retrieve_category(self, api_client, organization):
        """Test retrieving a specific category."""
        parent_category = Category.objects.create(organization=organization, name="Parent Category")
        category = Category.objects.create(organization=organization, name="Child Category", parent=parent_category)

        response = api_client.get(f"/api/catalog/categories/{category.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Child Category"
        assert response.data["parent_name"] == "Parent Category"

    def test_update_category(self, api_client, organization):
        """Test updating a specific category."""
        category = Category.objects.create(organization=organization, name="Old Category Name")
        data = {"name": "Updated Category Name"}

        response = api_client.patch(f"/api/catalog/categories/{category.id}/", data)
        assert response.status_code == status.HTTP_200_OK
        category.refresh_from_db()
        assert category.name == "Updated Category Name"

    def test_delete_category(self, api_client, organization):
        """Test deleting a specific category."""
        category = Category.objects.create(organization=organization, name="Category to Delete")

        response = api_client.delete(f"/api/catalog/categories/{category.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Category.objects.filter(name="Category to Delete").exists()




@pytest.mark.django_db
class TestProductViews:

    def test_list_products(self, api_client, organization):
        """Test listing products with organization filter."""
        Product.objects.create(organization=organization, name="Product 1", sku="SKU001")
        Product.objects.create(organization=organization, name="Product 2", sku="SKU002")

        response = api_client.get(f"/api/catalog/products/?org_id={organization.id}")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_create_product(self, api_client, organization):
        """Test creating a product with valid data."""
        data = {
            "organization": organization.id,
            "name": "New Product",
            "sku": "SKU123",
            "is_active": True
        }
        response = api_client.post("/api/catalog/products/create/", data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Product.objects.filter(name="New Product").exists()

    def test_retrieve_product(self, api_client, organization):
        """Test retrieving a specific product."""
        product = Product.objects.create(organization=organization, name="Product", sku="SKU123")

        response = api_client.get(f"/api/catalog/products/{product.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Product"

    def test_update_product(self, api_client, organization):
        """Test updating a specific product."""
        product = Product.objects.create(organization=organization, name="Old Product", sku="SKU123")
        data = {"name": "Updated Product"}

        response = api_client.patch(f"/api/catalog/products/{product.id}/", data)
        assert response.status_code == status.HTTP_200_OK
        product.refresh_from_db()
        assert product.name == "Updated Product"

    def test_delete_product(self, api_client, organization):
        """Test deleting a specific product."""
        product = Product.objects.create(organization=organization, name="Product to Delete", sku="SKU123")

        response = api_client.delete(f"/api/catalog/products/{product.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Product.objects.filter(name="Product to Delete").exists()


@pytest.mark.django_db
class TestProductImageViews:

    def test_list_product_images(self, api_client, product):
        """Test listing product images for a product."""
        # Create a simple in-memory image file
        test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61\x02\x00\x01\x00\x80\xff\x00\xff\x00\x00\x00\x00\x00\x21\xf9\x04\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x02\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b',
            # GIF image data
            content_type='image/gif'
        )
        ProductImage.objects.create(product=product, image=test_image, sorting=1)

        response = api_client.get(f"/api/catalog/product-images/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['product'] == product.id

    def test_create_product_image(self, api_client, product):
        """Test creating a product image with valid data, including an image file."""
        # Create a simple in-memory image file
        test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61\x02\x00\x01\x00\x80\xff\x00\xff\x00\x00\x00\x00\x00\x21\xf9\x04\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x02\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b',
            # Minimal GIF binary data
            content_type='image/gif'
        )

        data = {
            "product": product.id,
            "sorting": 1,
            "image": test_image
        }

        response = api_client.post("/api/catalog/product-images/", data, format='multipart')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['product'] == product.id
        assert 'image' in response.data  # Check if image URL is included in the response

    def test_retrieve_product_image(self, api_client, product):
        """Test retrieving a specific product image."""
        image = ProductImage.objects.create(product=product, sorting=1)

        response = api_client.get(f"/api/catalog/product-images/{image.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["sorting"] == 1

    def test_update_product_image(self, api_client, product):
        """Test updating a specific product image."""
        image = ProductImage.objects.create(product=product, sorting=1)
        data = {"sorting": 2}

        response = api_client.patch(f"/api/catalog/product-images/{image.id}/", data)
        assert response.status_code == status.HTTP_200_OK
        image.refresh_from_db()
        assert image.sorting == 2

    def test_delete_product_image(self, api_client, product):
        """Test deleting a specific product image."""
        image = ProductImage.objects.create(product=product, sorting=1)

        response = api_client.delete(f"/api/catalog/product-images/{image.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not ProductImage.objects.filter(id=image.id).exists()


@pytest.mark.django_db
class TestProductCostViews:

    def test_list_product_costs(self, api_client, product):
        """Test listing product costs for a product."""
        ProductCost.objects.create(product=product, amount=100, date="2024-10-01")

        response = api_client.get(f"/api/catalog/product-costs/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_create_product_cost(self, api_client, product, vendor):
        """Test creating a product cost with valid data."""
        data = {"product": product.id, "amount": "100.00", "date": "2024-10-01", "vendor": vendor.id}

        response = api_client.post("/api/catalog/product-costs/", data)
        assert response.status_code == status.HTTP_201_CREATED
        assert ProductCost.objects.filter(product=product).exists()

    def test_retrieve_product_cost(self, api_client, product):
        """Test retrieving a specific product cost."""
        cost = ProductCost.objects.create(product=product, amount=100, date="2024-10-01")

        response = api_client.get(f"/api/catalog/product-costs/{cost.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["amount"] == "100.00"

    def test_update_product_cost(self, api_client, product):
        """Test updating a specific product cost."""
        cost = ProductCost.objects.create(product=product, amount=100, date="2024-10-01")
        data = {"amount": "150.00"}

        response = api_client.patch(f"/api/catalog/product-costs/{cost.id}/", data)
        assert response.status_code == status.HTTP_200_OK
        cost.refresh_from_db()
        assert str(cost.amount) == "150.00"

    def test_delete_product_cost(self, api_client, product):
        """Test deleting a specific product cost."""
        cost = ProductCost.objects.create(product=product, amount=100, date="2024-10-01")

        response = api_client.delete(f"/api/catalog/product-costs/{cost.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not ProductCost.objects.filter(id=cost.id).exists()


@pytest.mark.django_db
class TestProductPriceViews:

    def test_list_product_prices(self, api_client, product):
        """Test listing product prices for a product."""
        ProductPrice.objects.create(product=product, amount=150, date="2024-10-01")

        response = api_client.get(f"/api/catalog/product-prices/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_create_product_price(self, api_client, product):
        """Test creating a product price with valid data."""
        data = {"product": product.id, "amount": "150.00", "date": "2024-10-01"}

        response = api_client.post("/api/catalog/product-prices/", data)
        assert response.status_code == status.HTTP_201_CREATED
        assert ProductPrice.objects.filter(product=product).exists()

    def test_retrieve_product_price(self, api_client, product):
        """Test retrieving a specific product price."""
        price = ProductPrice.objects.create(product=product, amount=150, date="2024-10-01")

        response = api_client.get(f"/api/catalog/product-prices/{price.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["amount"] == "150.00"

    def test_update_product_price(self, api_client, product):
        """Test updating a specific product price."""
        price = ProductPrice.objects.create(product=product, amount=150, date="2024-10-01")
        data = {"amount": "200.00"}

        response = api_client.patch(f"/api/catalog/product-prices/{price.id}/", data)
        assert response.status_code == status.HTTP_200_OK
        price.refresh_from_db()
        assert str(price.amount) == "200.00"

    def test_delete_product_price(self, api_client, product):
        """Test deleting a specific product price."""
        price = ProductPrice.objects.create(product=product, amount=150, date="2024-10-01")

        response = api_client.delete(f"/api/catalog/product-prices/{price.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not ProductPrice.objects.filter(id=price.id).exists()


