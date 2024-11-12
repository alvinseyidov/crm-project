import pytest
from decimal import Decimal
from purchase.models import Purchase, LandedCost, PurchaseItem, PurchaseReceive, PurchaseReceiveItem
from datetime import date



@pytest.fixture
def purchase(organization, vendor):
    return Purchase.objects.create(
        organization=organization,
        vendor=vendor,
        order_number="PO12345",
        currency="AZN",
        purchase_origin="local",
        allocation_method="proportional_value",
        date=date.today()
    )



@pytest.fixture
def landed_cost(organization, purchase):
    return LandedCost.objects.create(
        organization=organization,
        purchase=purchase,
        cost_type="customs_fee",
        amount=Decimal("150.00")
    )

@pytest.fixture
def purchase_item(purchase, product, tax):
    return PurchaseItem.objects.create(
        purchase=purchase,
        product=product,
        quantity=10,
        unit_cost=100,
        discount_amount=5,
        allocated_landed_cost=15,
        weight=2.5,
        volume=0.3,
        tax=tax
    )


@pytest.fixture
def purchase_receive(purchase, organization):
    return PurchaseReceive.objects.create(
        purchase=purchase,
        organization=organization,
        status="received",
        total_received_quantity=Decimal("100.00"),
        remarks="Test receive"
    )

@pytest.fixture
def purchase_receive_item(purchase_receive, product):
    return PurchaseReceiveItem.objects.create(
        purchase_receive=purchase_receive,
        product=product,
        ordered_quantity=Decimal("10.00"),
        received_quantity=Decimal("5.00")
    )
