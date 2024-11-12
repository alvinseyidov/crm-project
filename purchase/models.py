from decimal import Decimal

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.conf import settings
from inventory.models import Stock, Warehouse


def validate_image(image):
    max_size = 2 * 1024 * 1024  # 2 MB
    if image.size > max_size:
        raise ValidationError("Image file too large (max 2 MB)")

class Vendor(models.Model):
    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE,
        related_name='vendors'
    )
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    country = models.ForeignKey("core.Country", on_delete=models.SET_NULL,blank=True, null=True, related_name="vendors")
    tin = models.CharField(max_length=255, blank=True, null=True)  # VOEN
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    logo_image = models.ImageField(upload_to='vendor_logos/', blank=True, null=True, validators=[validate_image])

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class Purchase(models.Model):
    INVENTORY_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('received', 'Received'),
        ('canceled', 'Canceled'),
    ]

    CURRENCY = [
        ('USD', 'USD'),
        ('AZN', 'AZN'),
        ('TL', 'TL'),
        ('RBL', 'RBL'),
        ('EUR', 'EUR'),
    ]
    TYPE = [
        ('product', 'Məhsul alışı'),
        ('service', 'Xidmət alışı'),
    ]
    ORIGIN_CHOICES = [
        ('local', 'Ölkə daxili'),
        ('import', 'Ölkə xarici')
    ]
    ALLOCATION_METHOD_CHOICES = [
        ('proportional_value', 'Proportional to Item Value'),
        ('quantity_based', 'Quantity-Based Allocation'),
        ('weight_based', 'Weight-Based Allocation'),
        ('volume_based', 'Volume-Based Allocation')
    ]

    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE,
        related_name='purchases'
    )
    purchase_type = models.CharField(max_length=10, default='product', choices=TYPE)
    vendor = models.ForeignKey(
        'Vendor',
        on_delete=models.CASCADE,
        related_name='purchases'
    )
    order_number = models.CharField(max_length=255)
    customs_reference_number = models.CharField(max_length=255, blank=True, null=True)
    customs_payment_term = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    currency = models.CharField(default="AZN", max_length=3, choices=CURRENCY)
    currency_rate = models.DecimalField(max_digits=8, decimal_places=2,default=1)
    purchase_origin = models.CharField(max_length=10, choices=ORIGIN_CHOICES, default='local')
    allocation_method = models.CharField(
        max_length=20,
        choices=ALLOCATION_METHOD_CHOICES,
        default='proportional_value'
    )
    date = models.DateField()
    expected_delivery_date = models.DateField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=INVENTORY_STATUS_CHOICES,
        default='pending'
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.0
    )
    tax_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        default=0.0
    )
    grand_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date',)
        constraints = [
            models.UniqueConstraint(fields=['order_number', 'organization'],
                                    name='unique_order_number_per_organization'),
        ]

    @property
    def total_cost(self):
        """Calculate the total cost by summing the item_total_cost of all related PurchaseItems."""
        return self.items.aggregate(total=models.Sum('item_total_cost'))['total'] or 0
    def save(self, *args, **kwargs):
        if self.pk:  # Check if the instance already exists (it's being updated)
            old_status = Purchase.objects.get(pk=self.pk).status

            # Prevent changing status back to 'pending'
            if self.status == 'pending' and old_status != 'pending':
                raise ValueError("Status cannot be changed back to 'pending' once it has been updated.")

            # Allow only transition to 'canceled' after 'received'
            if old_status == 'received' and self.status not in ['canceled', 'received']:
                raise ValueError("Status can only be changed to 'canceled' after being 'received'.")

            # Prevent any status change after it has been 'canceled'
            if old_status == 'canceled' and self.status != 'canceled':
                raise ValueError("Status cannot be changed from 'canceled'.")
        # Ensure customs_fee and import_fee are set before saving purchase items
        if not self.pk and self.status != 'pending':
            raise ValueError("Status cannot be other than 'pending' when it is created.")
        if self.pk and not self.items.exists():
            self.status = 'pending'

        super().save(*args, **kwargs)
        # After the purchase is saved, update each purchase item to allocate the fees
        self.allocate_landed_costs()
        for item in self.items.all():
            item.save()  # This will recalculate each item's cost based on the new purchase info

    def finalize_purchase(self):
        self.save()

    def allocate_landed_costs(self):
        allocation_method = self.allocation_method
        items = self.items.all()
        item_updates = []

        # Reset allocated landed cost for all items
        items.update(allocated_landed_cost=0)
        items.update(vat_applicable_cost=0)

        # Calculate totals for allocation
        total_order_value = sum(item.converted_unit_cost * item.quantity for item in items if item.unit_cost)
        total_quantity = sum(item.quantity for item in items if item.quantity)
        total_weight = sum(item.weight for item in items if item.weight and item.weight > 0)
        total_volume = sum(item.volume for item in items if item.volume and item.volume > 0)

        # Determine available data for allocation
        weights_available = total_weight > 0
        volumes_available = total_volume > 0

        # Adjust allocation method if necessary
        if allocation_method == 'proportional_value' and total_order_value == 0:
            allocation_method = 'quantity_based'  # Fallback if order value is zero
        if allocation_method == 'weight_based' and not weights_available:
            allocation_method = 'quantity_based'  # Fallback if weight data is zero or unavailable
        if allocation_method == 'volume_based' and not volumes_available:
            allocation_method = 'quantity_based'  # Fallback if volume data is zero or unavailable

        # Calculate item shares based on the selected allocation method
        item_shares = {}
        for item in items:
            if allocation_method == 'proportional_value' and total_order_value:
                item_shares[item.id] = (item.converted_unit_cost * item.quantity) / total_order_value
            elif allocation_method == 'quantity_based' and total_quantity:
                item_shares[item.id] = item.quantity / total_quantity
            elif allocation_method == 'weight_based' and weights_available:
                item_shares[item.id] = item.weight / total_weight
            elif allocation_method == 'volume_based' and volumes_available:
                item_shares[item.id] = item.volume / total_volume
            else:
                item_shares[item.id] = 0  # Default to zero if no valid allocation method is available

        # Distribute each landed cost based on precomputed shares
        for landed_cost in self.landed_costs.all():
            amount = landed_cost.amount
            for item in items:
                item.allocated_landed_cost += item_shares[item.id] * amount
                item.calculate_item_total_cost()  # Update the total cost per item
                item_updates.append(item)
                if landed_cost.apply_vat:
                    item.vat_applicable_cost += item_shares[item.id] * amount
                    item.calculate_item_total_cost()  # Update the total cost per item
                    item_updates.append(item)
        PurchaseItem.objects.bulk_update(item_updates,
                                         ['allocated_landed_cost', 'vat_applicable_cost', 'item_total_cost'])
    def __str__(self):
        return f"{self.order_number} ({self.vendor.name})"



class PurchaseItem(models.Model):
    purchase = models.ForeignKey(
        'Purchase',
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        'catalog.Product',
        on_delete=models.CASCADE,
        related_name='purchase_items'
    )
    quantity = models.DecimalField(max_digits=12, decimal_places=2, default=1)
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2)
    converted_unit_cost = models.DecimalField(max_digits=15, decimal_places=2, editable=False)
    item_total_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.0
    )


    tax_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True
    )
    discount_amount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )
    allocated_landed_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vat_applicable_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Total cost that is applicable for VAT calculation")
    grand_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    weight = models.DecimalField(verbose_name="Çəki(kg)",max_digits=10, decimal_places=2, default=0)
    volume = models.DecimalField(verbose_name="Həcm (m3)",max_digits=10, decimal_places=2, default=0)

    tax = models.ForeignKey('accounting.Tax', on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_item_total_cost(self):
        """Calculate the base total cost of the item (quantity * unit_cost)."""
        self.item_total_cost = self.unit_cost * self.quantity * self.purchase.currency_rate
        self.converted_unit_cost = self.unit_cost * self.purchase.currency_rate
        return self.item_total_cost

    def calculate_grand_total(self):
        """Calculate the grand total with allocated landed cost, discount, and tax."""
        # Start with the base cost
        self.calculate_item_total_cost()  # Ensure item_total_cost is up-to-date

        # Add allocated landed cost
        total = self.item_total_cost + self.allocated_landed_cost

        # Apply discount if available
        if self.discount_amount:
            total -= self.discount_amount

        # Set the adjusted total before tax
        self.grand_total = total

        # Calculate and apply tax if applicable
        if self.tax and self.tax.percent:  # Assuming `rate` is a field in the Tax model (e.g., 0.18 for 18%)
            self.tax_amount = (self.item_total_cost + self.vat_applicable_cost) * self.tax.percent/100
        else:
            self.tax_amount = 0

        return self.grand_total

    def calculate_tax_amount(self):
        """Calculate the tax amount based on the grand total after discounts and allocated cost."""
        if self.tax and self.tax.percent:
            self.tax_amount = (self.item_total_cost + self.vat_applicable_cost) * self.tax.percent/100
        else:
            self.tax_amount = 0
        return self.tax_amount

    def save(self, *args, **kwargs):
        # Calculate base cost and grand total before saving
        if not self.tax and self.product.tax:
            self.tax = self.product.tax
        self.calculate_item_total_cost()
        self.calculate_grand_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"



class PurchaseDocument(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to='purchase_documents/')
    description = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Document for Purchase {self.purchase.id}'


class LandedCost(models.Model):
    COST_TYPE_CHOICES = [
        ('customs_fee', 'Customs Fee'),
        ('logistics', 'Logistics Cost'),
        ('customs_levy', 'Customs Levy'),  # Translated to "Customs Levy" in English
        ('other', 'Other')
    ]

    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE,
        related_name='landed_costs'
    )
    purchase = models.ForeignKey(
        'Purchase',
        on_delete=models.CASCADE,
        related_name='landed_costs'
    )
    cost_type = models.CharField(max_length=20, choices=COST_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    document = models.FileField(null=True, blank=True)
    apply_vat = models.BooleanField(default=True, help_text="Indicates if VAT should be applied to this cost")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_cost_type_display()} - {self.amount}"




class PurchaseReceive(models.Model):
    STATUS_CHOICES = [
        ('received', 'Received'),
        ('partially_received', 'Partially Received'),
        ('canceled', 'Canceled'),
    ]
    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE,
        related_name='purchase_receives'
    )
    purchase = models.ForeignKey(
        'Purchase',
        on_delete=models.CASCADE,
        related_name='receives'
    )
    warehouse = models.ForeignKey(
        'inventory.Warehouse',
        on_delete=models.SET_NULL,
        related_name='receives',
        null=True,
        blank=True
    )
    receive_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_received_quantity = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    remarks = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        warehouse = self.organization.warehouses.first()
        if not warehouse:
            warehouse = Warehouse.objects.create(name="Main Warehouse", organization=self.organization)
        if not self.warehouse:
            self.warehouse = warehouse
        super().save(*args, **kwargs)

    def update_received_quantity(self):
        """Calculate and update the total received quantity based on received items."""
        self.total_received_quantity = sum(item.received_quantity for item in self.receive_items.all())
        self.save()

    def __str__(self):
        return f"Receive for {self.purchase.order_number} - Status: {self.get_status_display()}"


class PurchaseReceiveItem(models.Model):
    purchase_receive = models.ForeignKey(
        PurchaseReceive,
        on_delete=models.CASCADE,
        related_name='receive_items'
    )
    product = models.ForeignKey(
        'catalog.Product',
        on_delete=models.CASCADE,
        related_name='received_items'
    )
    ordered_quantity = models.DecimalField(max_digits=12, decimal_places=2)
    received_quantity = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_fully_received = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Check if the received quantity meets or exceeds ordered quantity
        self.is_fully_received = self.received_quantity >= self.ordered_quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Received {self.received_quantity:.2f}/{self.ordered_quantity:.2f} of {self.product.name}"


class PurchaseReturn(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('processed', 'Processed'),
        ('canceled', 'Canceled'),
    ]

    purchase_order = models.ForeignKey(Purchase, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchase_returns')
    return_number = models.CharField(max_length=255, unique=True)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    reason = models.TextField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, default=0.0)
    grand_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        last_return = PurchaseReturn.objects.filter(purchase_order=self.purchase_order).order_by('id').last()

        if last_return:
            last_return_number = last_return.return_number.split('-')[-1]
            return_int = int(last_return_number[1:])
            new_return_number = f'PR{return_int + 1:06d}'
        else:
            new_return_number = 'PR000001'
        self.return_number = f'{self.purchase_order.order_number}-{new_return_number}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.return_number} (PurchaseOrder: {self.purchase_order.order_number})"



class PurchaseReturnItem(models.Model):
    purchase_return = models.ForeignKey(PurchaseReturn, on_delete=models.CASCADE, related_name='purchase_return_items')
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    price_per_unit = models.DecimalField(max_digits=12, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    tax = models.ForeignKey('accounting.Tax', on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.price_per_unit
        if self.tax:
            self.tax_amount = self.total_price * (self.tax.percent / 100)
        else:
            self.tax_amount = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Return {self.product.name} ({self.quantity})"






class Bill(models.Model):
    STATUS_DRAFT = 'draft'
    STATUS_ISSUED = 'issued'
    STATUS_PARTIALLY_PAID = 'partially_paid'
    STATUS_PAID = 'paid'
    STATUS_OVERDUE = 'overdue'

    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_ISSUED, 'Issued'),
        (STATUS_PARTIALLY_PAID, 'Partially Paid'),
        (STATUS_PAID, 'Paid'),
        (STATUS_OVERDUE, 'Overdue'),
    ]

    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="bills",
                                       verbose_name=_("Purchase Order"))
    bill_number = models.CharField(max_length=20, verbose_name=_("Invoice Number"))
    supplier = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='bills',
                                 verbose_name=_("Supplier"))
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE,
                                     related_name='bills', verbose_name=_("Organization"))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Total Amount"))
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name=_("Paid Amount"))
    remaining_balance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Remaining Balance"))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ISSUED, verbose_name=_("Status"))
    issued_date = models.DateField(null=True, blank=True, verbose_name=_("Issued Date"))
    due_date = models.DateField(null=True, blank=True, verbose_name=_("Due Date"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        constraints = [
            models.UniqueConstraint(fields=['bill_number', 'organization'], name='unique_bill_number_per_organization'),
        ]




    def __str__(self):
        return f"Purchase Bill {self.bill_number} - {self.supplier}"






