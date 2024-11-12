from rest_framework.test import APITestCase
from organization.models import Organization
from purchase.models import Vendor
from core.models import Country
import pytest
from decimal import Decimal
from purchase.models import LandedCost,PurchaseItem, Purchase, PurchaseReceive, PurchaseReceiveItem
from purchase.api.serializers import *
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.exceptions import ValidationError
from organization.models import Organization



class VendorSerializerTest(APITestCase):

    def setUp(self):
        self.organization = Organization.objects.create(name="Test Org")
        self.country = Country.objects.create(name="Test Country")
        self.vendor_data = {
            "organization": self.organization.id,
            "name": "Serialized Vendor",
            "email": "vendor@example.com",
            "phone": "123456789",
            "address": "123 Vendor Street",
            "country": self.country.id,
            "tin": "1234567890",
            "contact_person": "John Doe",
            "description": "A serialized test vendor",
            "is_active": True
        }

    def test_valid_vendor_serializer(self):
        serializer = VendorSerializer(data=self.vendor_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["name"], "Serialized Vendor")

    def test_invalid_vendor_serializer(self):
        invalid_data = self.vendor_data.copy()
        invalid_data["name"] = ""  # Name is required
        serializer = VendorSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)






@pytest.fixture
def valid_landed_cost_data(organization, purchase):
    return {
        "organization": organization.id,
        "purchase": purchase.id,
        "cost_type": "customs_fee",
        "amount": "150.00",
        "description": "Customs fee for import",
    }


@pytest.mark.django_db
class TestLandedCostSerializer:
    def test_valid_data(self, valid_landed_cost_data):
        """Test LandedCostSerializer with valid data."""
        serializer = LandedCostSerializer(data=valid_landed_cost_data)
        assert serializer.is_valid(), serializer.errors
        landed_cost = serializer.save()

        # Check saved fields
        assert landed_cost.cost_type == valid_landed_cost_data["cost_type"]
        assert landed_cost.amount == Decimal(valid_landed_cost_data["amount"])
        assert landed_cost.description == valid_landed_cost_data["description"]

    def test_missing_required_fields(self):
        """Test LandedCostSerializer with missing required fields."""
        invalid_data = {
            "cost_type": "logistics",  # Missing 'organization', 'purchase', and 'amount'
        }
        serializer = LandedCostSerializer(data=invalid_data)
        assert not serializer.is_valid()
        assert "organization" in serializer.errors
        assert "purchase" in serializer.errors
        assert "amount" in serializer.errors

    def test_invalid_cost_type(self, valid_landed_cost_data):
        """Test LandedCostSerializer with an invalid cost_type choice."""
        invalid_data = valid_landed_cost_data.copy()
        invalid_data["cost_type"] = "invalid_choice"
        serializer = LandedCostSerializer(data=invalid_data)
        assert not serializer.is_valid()
        assert "cost_type" in serializer.errors

    def test_file_upload(self, valid_landed_cost_data):
        """Test LandedCostSerializer with a file upload."""
        # Add a sample file to the data
        valid_landed_cost_data["document"] = SimpleUploadedFile(
            "test_file.pdf", b"File content", content_type="application/pdf"
        )
        serializer = LandedCostSerializer(data=valid_landed_cost_data)
        assert serializer.is_valid(), serializer.errors
        landed_cost = serializer.save()

        # Check that the file was saved correctly with the correct start and extension
        assert landed_cost.document.name.startswith("test_file")
        assert landed_cost.document.name.endswith(".pdf")

    def test_partial_update(self, organization, purchase):
        """Test partial update with LandedCostSerializer."""
        landed_cost = LandedCost.objects.create(
            organization=organization,
            purchase=purchase,
            cost_type="customs_fee",
            amount=Decimal("100.00")
        )
        update_data = {"amount": "200.00"}
        serializer = LandedCostSerializer(landed_cost, data=update_data, partial=True)
        assert serializer.is_valid(), serializer.errors
        updated_cost = serializer.save()

        # Check that the amount was updated
        assert updated_cost.amount == Decimal("200.00")





@pytest.mark.django_db
class TestPurchaseItemSerializer:

    def test_valid_data(self, purchase, product, tax):
        """Test PurchaseItemSerializer with valid data."""
        data = {
            "purchase": purchase.id,
            "product": product.id,
            "quantity": "10.00",
            "unit_cost": "100.00",
            "discount_amount": "5.00",
            "allocated_landed_cost": "15.00",
            "weight": "2.5",
            "volume": "0.3",
            "tax": tax.id
        }
        serializer = PurchaseItemSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        item = serializer.save()

        # Check values
        assert item.product.id == product.id
        assert item.quantity == Decimal("10.00")
        assert item.unit_cost == Decimal("100.00")
        assert item.discount_amount == Decimal("5.00")
        assert item.allocated_landed_cost == Decimal("15.00")
        assert item.weight == Decimal("2.5")
        assert item.volume == Decimal("0.3")

    def test_read_only_fields(self, purchase_item):
        """Test that read-only fields are not included in validated data."""
        serializer = PurchaseItemSerializer(instance=purchase_item)
        data = serializer.data

        # Ensure read-only fields are present in serialized data
        assert "item_total_cost" in data
        assert "grand_total" in data
        assert "tax_amount" in data
        assert "product_name" in data
        assert "tax_display" in data
        assert "tax_percent" in data




@pytest.mark.django_db
class TestPurchaseCreateSerializer:

    def test_valid_data(self, organization, vendor):
        """Test PurchaseCreateSerializer with valid data."""
        data = {
            "organization": organization.id,
            "vendor": vendor.id,
            "order_number": "PO123",
            "currency": "USD",
            "currency_rate": "1.00",
            "date": "2024-11-01",
            "status": "pending",
            "payment_status": "invoiced",
            "total_amount": "1000.00",
            "tax_amount": "80.00",
            "grand_total": "1080.00",
            "description": "Test purchase"
        }
        serializer = PurchaseCreateSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        purchase = serializer.save()

        # Check values
        assert purchase.vendor.id == vendor.id
        assert purchase.currency == "USD"
        assert purchase.currency_rate == Decimal("1.00")
        assert purchase.total_amount == Decimal("1000.00")
        assert purchase.grand_total == Decimal("1080.00")

    def test_missing_required_fields(self):
        """Test PurchaseCreateSerializer with missing required fields."""
        data = {"order_number": "PO123"}
        serializer = PurchaseCreateSerializer(data=data)
        assert not serializer.is_valid()
        assert "organization" in serializer.errors
        assert "vendor" in serializer.errors





@pytest.mark.django_db
class TestPurchaseListSerializer:

    def test_purchase_list_fields(self, purchase):
        """Test PurchaseListSerializer output format."""
        serializer = PurchaseListSerializer(instance=purchase)
        data = serializer.data

        # Verify standard fields and display fields
        assert "vendor" in data
        assert "status_display" in data
        assert "payment_status_display" in data
        assert "purchase_origin_display" in data
        assert "allocation_method_display" in data






@pytest.mark.django_db
class TestPurchaseDetailSerializer:

    def test_purchase_detail_fields(self, purchase, purchase_item, landed_cost):
        """Test PurchaseDetailSerializer output format."""
        purchase.items.add(purchase_item)
        purchase.landed_costs.add(landed_cost)
        serializer = PurchaseDetailSerializer(instance=purchase)
        data = serializer.data

        # Verify fields and related data
        assert "vendor" in data
        assert "items" in data
        assert "landed_costs" in data
        assert data["items"][0]["product_name"] == purchase_item.product.name




@pytest.mark.django_db
class TestPurchaseReceiveItemSerializer:

    def test_purchase_receive_item_serialization(self, purchase_receive, product):
        """Test serialization of PurchaseReceiveItem data."""
        receive_item = PurchaseReceiveItem.objects.create(
            purchase_receive=purchase_receive,
            product=product,
            ordered_quantity=10,
            received_quantity=5
        )
        serializer = PurchaseReceiveItemSerializer(receive_item)
        data = serializer.data
        assert data['ordered_quantity'] == "10.00"  # Compare with string
        assert data['received_quantity'] == "5.00"  # Compare with string
        assert data['is_fully_received'] is False

    def test_purchase_receive_item_validation(self, purchase_receive, product):
        """Test that received_quantity validation works correctly."""
        receive_item = PurchaseReceiveItem(
            purchase_receive=purchase_receive,
            product=product,
            ordered_quantity=10,
            received_quantity=15  # Exceeds ordered quantity
        )
        serializer = PurchaseReceiveItemSerializer(instance=receive_item)
        with pytest.raises(ValidationError) as excinfo:
            serializer.validate_received_quantity(15)
        assert "Received quantity cannot exceed ordered quantity." in str(excinfo.value)


@pytest.mark.django_db
class TestPurchaseReceiveItemDetailSerializer:

    def test_purchase_receive_item_detail_serialization(self, purchase_receive, product):
        """Test that PurchaseReceiveItemDetailSerializer correctly serializes with product name."""
        receive_item = PurchaseReceiveItem.objects.create(
            purchase_receive=purchase_receive,
            product=product,
            ordered_quantity=10,
            received_quantity=5
        )
        serializer = PurchaseReceiveItemDetailSerializer(receive_item)
        data = serializer.data
        assert data['product_name'] == product.name
        assert data['ordered_quantity'] == "10.00"  # Compare with string
        assert data['received_quantity'] == "5.00"  # Compare with string
        assert data['is_fully_received'] is False


@pytest.mark.django_db
class TestPurchaseReceiveSerializer:

    def test_purchase_receive_serialization(self, purchase, organization):
        """Test serialization of PurchaseReceive data."""
        purchase_receive = PurchaseReceive.objects.create(
            purchase=purchase,
            organization=organization,
            status="received",
            total_received_quantity=Decimal("100.00"),
            remarks="Initial full receive"
        )
        serializer = PurchaseReceiveSerializer(purchase_receive)
        data = serializer.data
        assert data['status'] == "received"
        assert data['total_received_quantity'] == "100.00"  # Compare with string
        assert data['remarks'] == "Initial full receive"

    def test_purchase_receive_update(self, purchase_receive):
        """Test the update method of PurchaseReceiveSerializer to verify total quantity update."""
        purchase_receive.total_received_quantity = 50
        purchase_receive.save()

        serializer = PurchaseReceiveSerializer(
            instance=purchase_receive,
            data={'status': 'partially_received'},
            partial=True
        )
        assert serializer.is_valid()
        serializer.save()
        purchase_receive.refresh_from_db()
        assert purchase_receive.status == 'partially_received'


@pytest.mark.django_db
class TestPurchaseReceiveDetailSerializer:

    def test_purchase_receive_detail_serialization(self, purchase, organization, product):
        """Test that PurchaseReceiveDetailSerializer correctly serializes with all item details."""
        purchase_receive = PurchaseReceive.objects.create(
            purchase=purchase,
            organization=organization,
            status="received",
            total_received_quantity=Decimal("100.00"),
            remarks="Initial full receive"
        )
        receive_item = PurchaseReceiveItem.objects.create(
            purchase_receive=purchase_receive,
            product=product,
            ordered_quantity=10,
            received_quantity=5
        )

        serializer = PurchaseReceiveDetailSerializer(purchase_receive)
        data = serializer.data

        # Check top-level fields
        assert data['status'] == "received"
        assert data['total_received_quantity'] == "100.00"  # Compare with string
        assert data['remarks'] == "Initial full receive"

        # Check nested receive_items
        assert len(data['receive_items']) == 1
        assert data['receive_items'][0]['product_name'] == product.name
        assert data['receive_items'][0]['ordered_quantity'] == "10.00"  # Compare with string
        assert data['receive_items'][0]['received_quantity'] == "5.00"  # Compare with string
        assert data['receive_items'][0]['is_fully_received'] is False
