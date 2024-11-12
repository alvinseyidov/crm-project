import pytest
from rest_framework import status
from purchase.models import *
from decimal import Decimal
from django.urls import reverse
from purchase.models import LandedCost
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from purchase.models import Purchase



@pytest.mark.django_db
class TestVendorViews:

    def test_list_vendors(self, api_client, organization, country):
        """Test listing vendors with organization filter."""
        Vendor.objects.create(organization=organization, name="Vendor 1", country=country)
        Vendor.objects.create(organization=organization, name="Vendor 2", country=country)

        # Make an authenticated GET request with the organization filter
        response = api_client.get(f"/api/purchase/vendors/?org_id={organization.id}")

        # Validate response
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_create_vendor(self, api_client, organization, country):
        """Test creating a vendor with valid data."""
        data = {
            "organization": organization.id,
            "name": "New Vendor",
            "country": country.id,
            "email": "vendor@example.com",
            "phone": "1234567890",
            "address": "123 Vendor Street",
            "tin": "123456789",
            "contact_person": "John Doe",
            "description": "A test vendor",
            "is_active": True
        }
        response = api_client.post("/api/purchase/vendors/", data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Vendor.objects.filter(name="New Vendor").exists()

    def test_retrieve_vendor(self, api_client, organization, country):
        """Test retrieving a specific vendor."""
        vendor = Vendor.objects.create(organization=organization, name="Vendor 1", country=country)
        response = api_client.get(f"/api/purchase/vendors/{vendor.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == vendor.name

    def test_update_vendor(self, api_client, organization, country):
        """Test updating a specific vendor."""
        vendor = Vendor.objects.create(organization=organization, name="Old Vendor", country=country)
        data = {"name": "Updated Vendor"}
        response = api_client.patch(f"/api/purchase/vendors/{vendor.id}/", data)
        assert response.status_code == status.HTTP_200_OK
        vendor.refresh_from_db()
        assert vendor.name == "Updated Vendor"

    def test_delete_vendor(self, api_client, organization, country):
        """Test deleting a specific vendor."""
        vendor = Vendor.objects.create(organization=organization, name="Vendor to Delete", country=country)
        response = api_client.delete(f"/api/purchase/vendors/{vendor.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Vendor.objects.filter(name="Vendor to Delete").exists()





@pytest.mark.django_db
class TestLandedCostViews:
    def test_list_landed_costs(self, api_client, organization, purchase):
        """Test listing landed costs with organization filter."""
        LandedCost.objects.create(organization=organization, purchase=purchase, cost_type="customs_fee", amount=Decimal("100.00"))
        LandedCost.objects.create(organization=organization, purchase=purchase, cost_type="logistics", amount=Decimal("200.00"))

        # Make a GET request with the organization filter
        response = api_client.get(f"/api/purchase/landed-costs/?org_id={organization.id}")

        # Validate response
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_create_landed_cost(self, api_client, organization, purchase):
        """Test creating a landed cost with valid data."""
        url = reverse('purchase-api:landed-costs-list-create')
        data = {
            "organization": organization.id,
            "purchase": purchase.id,
            "cost_type": "customs_levy",
            "amount": "150.00",
            "description": "Customs levy for import",
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert LandedCost.objects.filter(cost_type="customs_levy", amount=Decimal("150.00")).exists()

    def test_retrieve_landed_cost(self, api_client, organization, purchase):
        """Test retrieving a specific landed cost."""
        landed_cost = LandedCost.objects.create(organization=organization, purchase=purchase, cost_type="customs_fee", amount=Decimal("100.00"))
        url = reverse('purchase-api:landed-costs-detail', args=[landed_cost.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["cost_type"] == landed_cost.cost_type
        assert response.data["amount"] == str(landed_cost.amount)

    def test_update_landed_cost(self, api_client, organization, purchase):
        """Test updating a specific landed cost."""
        landed_cost = LandedCost.objects.create(organization=organization, purchase=purchase, cost_type="customs_fee", amount=Decimal("100.00"))
        url = reverse('purchase-api:landed-costs-detail', args=[landed_cost.id])
        data = {"amount": "200.00", "description": "Updated customs fee"}
        response = api_client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        landed_cost.refresh_from_db()
        assert landed_cost.amount == Decimal("200.00")
        assert landed_cost.description == "Updated customs fee"

    def test_delete_landed_cost(self, api_client, organization, purchase):
        """Test deleting a specific landed cost."""
        landed_cost = LandedCost.objects.create(organization=organization, purchase=purchase, cost_type="customs_fee", amount=Decimal("100.00"))
        url = reverse('purchase-api:landed-costs-detail', args=[landed_cost.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not LandedCost.objects.filter(id=landed_cost.id).exists()

    def test_create_landed_cost_with_file(self, api_client, organization, purchase):
        """Test creating a landed cost with a file upload."""
        url = reverse('purchase-api:landed-costs-list-create')
        data = {
            "organization": organization.id,
            "purchase": purchase.id,
            "cost_type": "logistics",
            "amount": "250.00",
            "description": "Logistics cost",
            "document": SimpleUploadedFile("test_file.pdf", b"File content", content_type="application/pdf")
        }
        response = api_client.post(url, data, format='multipart')
        assert response.status_code == status.HTTP_201_CREATED
        assert "document" in response.data
        assert response.data["cost_type"] == "logistics"




# Tests for Purchase Views
@pytest.mark.django_db
class TestPurchaseViews:

    def test_list_purchases(self, api_client, organization, vendor):
        """Test listing purchases with optional organization filter."""
        Purchase.objects.create(organization=organization, vendor=vendor, order_number="PO12345", date="2024-11-01")
        Purchase.objects.create(organization=organization, vendor=vendor, order_number="PO54321", date="2024-11-01")

        # Make an authenticated GET request with the organization filter
        url = reverse('purchase-api:purchase-list-create')
        response = api_client.get(url, {'org_id': organization.id})

        # Validate response
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_create_purchase(self, api_client, organization, vendor):
        """Test creating a purchase with valid data."""
        data = {
            "organization": organization.id,
            "vendor": vendor.id,
            "order_number": "PO67890",
            "currency": "USD",
            "currency_rate": "1.00",
            "date": "2024-11-01",
            "status": "pending",
            "payment_status": "invoiced",
            "total_amount": "1000.00",
            "grand_total": "1080.00",
            "description": "Test purchase"
        }
        url = reverse('purchase-api:purchase-list-create')
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Purchase.objects.filter(order_number="PO67890").exists()

    def test_retrieve_purchase(self, api_client, purchase):
        """Test retrieving a specific purchase."""
        url = reverse('purchase-api:purchase-detail', args=[purchase.id])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["order_number"] == purchase.order_number

    def test_update_purchase(self, api_client, purchase):
        """Test updating a specific purchase."""
        data = {"order_number": "PO98765"}
        url = reverse('purchase-api:purchase-detail', args=[purchase.id])
        response = api_client.patch(url, data)

        assert response.status_code == status.HTTP_200_OK
        purchase.refresh_from_db()
        assert purchase.order_number == "PO98765"

    def test_delete_purchase(self, api_client, purchase):
        """Test deleting a specific purchase."""
        url = reverse('purchase-api:purchase-detail', args=[purchase.id])
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Purchase.objects.filter(id=purchase.id).exists()


# Tests for PurchaseItem Views
@pytest.mark.django_db
class TestPurchaseItemViews:

    def test_list_purchase_items(self, api_client, purchase, product):
        """Test listing purchase items with optional purchase filter."""
        PurchaseItem.objects.create(purchase=purchase, product=product, quantity=10, unit_cost=100)
        PurchaseItem.objects.create(purchase=purchase, product=product, quantity=5, unit_cost=200)

        # Make an authenticated GET request with the purchase filter
        url = reverse('purchase-api:purchaseitem-list-create')
        response = api_client.get(url, {'purchase_id': purchase.id})

        # Validate response
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_create_purchase_item(self, api_client, purchase, product):
        """Test creating a purchase item with valid data."""
        data = {
            "purchase": purchase.id,
            "product": product.id,
            "quantity": "10",
            "unit_cost": "100",
            "discount_amount": "5",
            "allocated_landed_cost": "15",
            "weight": "2.5",
            "volume": "0.3"
        }
        url = reverse('purchase-api:purchaseitem-list-create')
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert PurchaseItem.objects.filter(purchase=purchase, product=product).exists()

    def test_retrieve_purchase_item(self, api_client, purchase_item):
        """Test retrieving a specific purchase item."""
        url = reverse('purchase-api:purchaseitem-detail', args=[purchase_item.id])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["quantity"] == format(purchase_item.quantity, '.2f')  # Match decimal format like '10.00'

    def test_update_purchase_item(self, api_client, purchase_item):
        """Test updating a specific purchase item."""
        data = {"quantity": "15"}
        url = reverse('purchase-api:purchaseitem-detail', args=[purchase_item.id])
        response = api_client.patch(url, data)

        assert response.status_code == status.HTTP_200_OK
        purchase_item.refresh_from_db()
        assert purchase_item.quantity == 15

    def test_delete_purchase_item(self, api_client, purchase_item):
        """Test deleting a specific purchase item."""
        url = reverse('purchase-api:purchaseitem-detail', args=[purchase_item.id])
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not PurchaseItem.objects.filter(id=purchase_item.id).exists()




@pytest.mark.django_db
class TestPurchaseReceiveViews:

    def test_purchase_receive_list_create(self, api_client, purchase, organization):
        """Test listing and creating purchase receive records."""
        # Test listing
        url = reverse('purchase-api:purchase-receive-list-create')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        # Test creation
        data = {
            "purchase": purchase.id,
            "organization": organization.id,
            "status": "received",
            "remarks": "Test receive"
        }
        response = api_client.post(url, data=data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["status"] == "received"
        assert response.data["total_received_quantity"] == "0.00"  # Check default value

    def test_purchase_receive_retrieve_update_delete(self, api_client, purchase_receive, purchase, organization):
        """Test retrieving, updating, and deleting a purchase receive record."""
        # Test retrieve
        url = reverse('purchase-api:purchase-receive-detail', args=[purchase_receive.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == purchase_receive.id

        # Test update
        update_data = {"status": "partially_received", "remarks": "Updated remarks"}
        response = api_client.patch(url, data=update_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == "partially_received"
        assert response.data["remarks"] == "Updated remarks"

        # Test delete
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not PurchaseReceive.objects.filter(id=purchase_receive.id).exists()


@pytest.mark.django_db
class TestPurchaseReceiveItemViews:



    def test_purchase_receive_item_list_create(self, api_client, purchase_receive, product):
        """Test listing and creating purchase receive item records."""
        # Test listing
        url = reverse('purchase-api:purchase-receive-item-list-create')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        # Test creation
        data = {
            "purchase_receive": purchase_receive.id,
            "product": product.id,
            "ordered_quantity": "10.00",
            "received_quantity": "5.00",
        }
        response = api_client.post(url, data=data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["ordered_quantity"] == "10.00"
        assert response.data["received_quantity"] == "5.00"

    def test_purchase_receive_item_retrieve_update_delete(self, api_client, purchase_receive_item):
        """Test retrieving, updating, and deleting a purchase receive item record."""
        # Test retrieve
        url = reverse('purchase-api:purchase-receive-item-detail', args=[purchase_receive_item.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == purchase_receive_item.id

        # Test update
        update_data = {"received_quantity": "7.00"}
        response = api_client.patch(url, data=update_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data["received_quantity"] == "7.00"

        # Test delete
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not PurchaseReceiveItem.objects.filter(id=purchase_receive_item.id).exists()
