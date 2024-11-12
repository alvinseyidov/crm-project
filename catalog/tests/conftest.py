# catalog/tests/conftest.py

import pytest
from django.contrib.auth import get_user_model

from catalog.models import Product, ProductAttributeValue, Brand, Manufacturer, Category, ProductAttribute
from organization.models import Organization
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient

from purchase.models import Vendor


# Fixture for authenticated API client with JWT
@pytest.fixture
def api_client():
    # Get the custom user model
    User = get_user_model()

    # Create a test user
    user = User.objects.create_user(email="testuser@gmail.com", password="testpassword")

    # Generate JWT token for the test user
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    # Set up the API client with the Authorization header
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return client


@pytest.fixture
def organization():
    return Organization.objects.create(name="Test Organization")

@pytest.fixture
def category(organization):
    return Category.objects.create(organization=organization, name="Electronics")

@pytest.fixture
def brand(organization):
    return Brand.objects.create(organization=organization, name="TechBrand")

@pytest.fixture
def manufacturer(organization):
    return Manufacturer.objects.create(organization=organization, name="TechManufacturer")

@pytest.fixture
def vendor(organization):
    return Vendor.objects.create(organization=organization, name="TechVendor")

@pytest.fixture
def attribute(organization):
    # Create a ProductAttribute first
    product_attribute = ProductAttribute.objects.create(organization=organization, name="Color")
    # Then, create ProductAttributeValue linked to this attribute
    return ProductAttributeValue.objects.create(attribute=product_attribute, value="Black")


@pytest.fixture
def product(organization, category, brand, manufacturer):
    return Product.objects.create(
        organization=organization,
        category=category,
        brand=brand,
        manufacturer=manufacturer,
        name="Test Product",
        sku="SKU123",
        measurement="pc",
        type="product",
        is_active=True
    )
