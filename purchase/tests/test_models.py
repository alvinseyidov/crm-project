from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
import pytest
from datetime import date
from organization.models import Organization
from purchase.models import *
from core.models import Country
from decimal import Decimal


class VendorModelTest(TestCase):

    def setUp(self):
        self.organization = Organization.objects.create(name="Test Org")
        self.country = Country.objects.create(name="Test Country")

    def test_vendor_creation(self):
        vendor = Vendor.objects.create(
            organization=self.organization,
            name="Test Vendor",
            email="vendor@example.com",
            phone="123456789",
            address="123 Vendor Street",
            country=self.country,
            tin="1234567890",
            contact_person="John Doe",
            description="A test vendor",
            is_active=True
        )
        self.assertEqual(vendor.name, "Test Vendor")
        self.assertEqual(vendor.organization, self.organization)

    def test_vendor_logo_image_size_validation(self):
        """Test that validation raises an error for logo images larger than 2 MB."""
        organization = Organization.objects.create(name="Test Organization")

        # Create a simulated large image file (e.g., 3 MB)
        large_image = SimpleUploadedFile(
            name='large_image.png',
            content=b'\x00' * (3 * 1024 * 1024),  # 3 MB
            content_type='image/png'
        )

        # Attempt to create a vendor with the large image
        with self.assertRaises(ValidationError):
            vendor = Vendor(
                organization=organization,
                name="Vendor with large image",
                logo_image=large_image
            )
            vendor.full_clean()  # This triggers the image size validation

    def test_str_method(self):
        vendor = Vendor.objects.create(organization=self.organization, name="String Test Vendor")
        self.assertEqual(str(vendor), "String Test Vendor")






@pytest.mark.django_db
class TestPurchaseModel:

    def test_purchase_creation(self, organization, vendor):
        """Test that a purchase can be created with basic fields."""
        purchase = Purchase.objects.create(
            organization=organization,
            vendor=vendor,
            order_number="PO123",
            currency="AZN",
            purchase_origin="local",
            date=date.today()
        )
        assert purchase.order_number == "PO123"
        assert purchase.currency == "AZN"
        assert purchase.purchase_origin == "local"

    def test_allocate_landed_costs_proportional_value(self, purchase, product, landed_cost):
        """Test landed cost allocation with proportional value method."""
        purchase.allocation_method = 'proportional_value'
        purchase.save()

        # Create purchase items with different unit costs
        item1 = PurchaseItem.objects.create(purchase=purchase, product=product, quantity=10, unit_cost=100)
        item2 = PurchaseItem.objects.create(purchase=purchase, product=product, quantity=5, unit_cost=200)

        purchase.allocate_landed_costs()  # Trigger allocation

        # Calculate expected shares
        total_order_value = item1.unit_cost * item1.quantity + item2.unit_cost * item2.quantity
        item1_share = (item1.unit_cost * item1.quantity) / total_order_value
        item2_share = (item2.unit_cost * item2.quantity) / total_order_value

        # Verify allocated costs
        expected_cost1 = landed_cost.amount * Decimal(item1_share)
        expected_cost2 = landed_cost.amount * Decimal(item2_share)
        item1.refresh_from_db()
        item2.refresh_from_db()
        assert item1.allocated_landed_cost == pytest.approx(expected_cost1, rel=1e-2)
        assert item2.allocated_landed_cost == pytest.approx(expected_cost2, rel=1e-2)

    def test_allocate_landed_costs_quantity_based(self, purchase, product, landed_cost):
        """Test landed cost allocation with quantity-based method."""
        purchase.allocation_method = 'quantity_based'
        purchase.save()

        item1 = PurchaseItem.objects.create(purchase=purchase, product=product, quantity=10, unit_cost=100)
        item2 = PurchaseItem.objects.create(purchase=purchase, product=product, quantity=5, unit_cost=200)

        purchase.allocate_landed_costs()

        # Calculate expected shares based on quantity
        total_quantity = item1.quantity + item2.quantity
        item1_share = item1.quantity / total_quantity
        item2_share = item2.quantity / total_quantity

        expected_cost1 = landed_cost.amount * Decimal(item1_share)
        expected_cost2 = landed_cost.amount * Decimal(item2_share)

        item1.refresh_from_db()
        item2.refresh_from_db()
        assert item1.allocated_landed_cost == pytest.approx(expected_cost1, rel=Decimal("0.01"))
        assert item2.allocated_landed_cost == pytest.approx(expected_cost2, rel=Decimal("0.01"))


@pytest.mark.django_db
class TestPurchaseItemModel:

    def test_item_total_cost_calculation(self, purchase, product):
        """Test calculation of item total cost based on quantity and unit cost."""
        item = PurchaseItem.objects.create(purchase=purchase, product=product, quantity=5, unit_cost=100)
        assert item.item_total_cost == item.quantity * item.unit_cost  # Should be 500

    def test_grand_total_with_discount_and_tax(self, purchase, product, tax):
        """Test grand total calculation with discount applied, excluding tax."""
        item = PurchaseItem.objects.create(
            purchase=purchase,
            product=product,
            quantity=5,
            unit_cost=100,
            discount_amount=50,
            tax=tax
        )
        item.calculate_grand_total()

        # Expected grand total: base cost - discount + allocated landed cost (without tax)
        expected_base = item.unit_cost * item.quantity  # 500
        expected_discounted = expected_base - item.discount_amount  # 450
        expected_grand_total = expected_discounted

        # Check grand total without tax
        assert item.grand_total == pytest.approx(expected_grand_total, rel=1e-2)

        # Check tax amount separately
        expected_tax = expected_discounted * (tax.percent / 100)
        assert item.tax_amount == pytest.approx(expected_tax, rel=1e-2)

    def test_tax_amount_calculation(self, purchase, product, tax):
        """Test that tax amount is calculated based on the tax rate."""
        item = PurchaseItem.objects.create(
            purchase=purchase,
            product=product,
            quantity=5,
            unit_cost=100,
            tax=tax
        )
        item.calculate_tax_amount()

        expected_tax_amount = (item.unit_cost * item.quantity) * (tax.percent / 100)
        assert item.tax_amount == pytest.approx(expected_tax_amount, rel=1e-2)


@pytest.mark.django_db
class TestLandedCostModel:

    def test_landed_cost_creation(self, organization, purchase):
        """Test that a landed cost can be created and linked to a purchase."""
        landed_cost = LandedCost.objects.create(
            organization=organization,
            purchase=purchase,
            cost_type="customs_fee",
            amount=Decimal("150.00")
        )
        assert landed_cost.cost_type == "customs_fee"
        assert landed_cost.amount == Decimal("150.00")
        assert landed_cost.purchase == purchase

@pytest.mark.django_db
class TestPurchaseReceiveModel:

    def test_purchase_receive_creation(self, purchase, organization):
        """Test that a purchase receive record can be created with basic fields."""
        purchase_receive = PurchaseReceive.objects.create(
            purchase=purchase,
            organization=organization,
            status="received",
            total_received_quantity=100,
            remarks="Initial full receive"
        )
        assert purchase_receive.purchase == purchase
        assert purchase_receive.organization == organization
        assert purchase_receive.status == "received"
        assert purchase_receive.total_received_quantity == Decimal("100.00")
        assert purchase_receive.remarks == "Initial full receive"

    def test_update_received_quantity(self, purchase, organization, product):
        """Test that total received quantity is updated based on received items."""
        purchase_receive = PurchaseReceive.objects.create(
            purchase=purchase,
            organization=organization
        )

        # Create PurchaseReceiveItems
        item1 = PurchaseReceiveItem.objects.create(
            purchase_receive=purchase_receive,
            product=product,
            ordered_quantity=10,
            received_quantity=7
        )
        item2 = PurchaseReceiveItem.objects.create(
            purchase_receive=purchase_receive,
            product=product,
            ordered_quantity=5,
            received_quantity=5
        )

        # Trigger the update and check the total received quantity
        purchase_receive.update_received_quantity()
        purchase_receive.refresh_from_db()
        assert purchase_receive.total_received_quantity == Decimal("12.00")  # 7 + 5

    def test_purchase_receive_str(self, purchase, organization):
        """Test the string representation of a purchase receive instance."""
        purchase_receive = PurchaseReceive.objects.create(
            purchase=purchase,
            organization=organization,
            status="partially_received"
        )
        assert str(purchase_receive) == f"Receive for {purchase.order_number} - Status: {purchase_receive.get_status_display()}"

@pytest.mark.django_db
class TestPurchaseReceiveItemModel:

    def test_purchase_receive_item_creation(self, purchase, organization, product):
        """Test that a purchase receive item can be created with basic fields."""
        purchase_receive = PurchaseReceive.objects.create(
            purchase=purchase,
            organization=organization
        )
        receive_item = PurchaseReceiveItem.objects.create(
            purchase_receive=purchase_receive,
            product=product,
            ordered_quantity=10,
            received_quantity=8
        )
        assert receive_item.purchase_receive == purchase_receive
        assert receive_item.product == product
        assert receive_item.ordered_quantity == Decimal("10.00")
        assert receive_item.received_quantity == Decimal("8.00")
        assert not receive_item.is_fully_received  # Because received_quantity < ordered_quantity

    def test_is_fully_received_update_on_save(self, purchase, organization, product):
        """Test that is_fully_received is correctly updated on save based on quantities."""
        purchase_receive = PurchaseReceive.objects.create(
            purchase=purchase,
            organization=organization
        )
        receive_item = PurchaseReceiveItem.objects.create(
            purchase_receive=purchase_receive,
            product=product,
            ordered_quantity=10,
            received_quantity=10
        )
        assert receive_item.is_fully_received  # Fully received since received_quantity == ordered_quantity

        # Update received quantity to less than ordered and save again
        receive_item.received_quantity = 5
        receive_item.save()
        receive_item.refresh_from_db()
        assert not receive_item.is_fully_received  # Now it should be False

    def test_purchase_receive_item_str(self, purchase, organization, product):
        """Test the string representation of a purchase receive item."""
        purchase_receive = PurchaseReceive.objects.create(
            purchase=purchase,
            organization=organization
        )
        receive_item = PurchaseReceiveItem.objects.create(
            purchase_receive=purchase_receive,
            product=product,
            ordered_quantity=10,
            received_quantity=5
        )
        assert str(receive_item) == f"Received 5.00/10.00 of {product.name}"