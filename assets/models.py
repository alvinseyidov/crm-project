from django.db import models
from django.utils.translation import gettext_lazy as _


class FixedAssetsCategory(models.Model):
    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE,
        related_name='fixed_asset_categories'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name



class FixedAssets(models.Model):
    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE,
        related_name='fixed_assets'
    )
    name = models.CharField(max_length=255)
    purchase_date = models.DateField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    asset_category = models.ForeignKey(FixedAssetsCategory, on_delete=models.SET_NULL, null=True)
    depreciation_rate = models.DecimalField(max_digits=5, decimal_places=2)
    serial_number = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class FixedAssetsPurchase(models.Model):
    CURRENCY = [
        ('USD', 'USD'),
        ('AZN', 'AZN'),
        ('TL', 'TL'),
        ('RBL', 'RBL'),
        ('EUR', 'EUR'),
    ]
    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE,
        related_name='fixed_asset_purchases'
    )
    vendor = models.ForeignKey(
        'purchase.Vendor',  # Assuming you have a Vendor model
        on_delete=models.CASCADE,
        related_name='fixed_asset_purchases'
    )
    purchase_date = models.DateField()
    total_cost = models.DecimalField(max_digits=12, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=12, decimal_places=2)
    payment_status = models.CharField(max_length=50, choices=[('paid', 'Paid'), ('pending', 'Pending')])
    currency = models.CharField(default="AZN", max_length=3, choices=CURRENCY)
    currency_rate = models.DecimalField(max_digits=8, decimal_places=2, default=1)

    ygb_number = models.CharField(max_length=255, blank=True, null=True)
    ygb_payment = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    customs_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    import_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    logistic_expenses = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Purchase on {self.purchase_date} - {self.organization.name}"

class FixedAssetsPurchaseItem(models.Model):
    fixed_asset_purchase = models.ForeignKey(
        FixedAssetsPurchase,
        on_delete=models.CASCADE,
        related_name='purchase_items'
    )
    asset = models.ForeignKey(
        FixedAssets,
        on_delete=models.SET_NULL,
        null=True
    )
    quantity = models.PositiveIntegerField(default=1)
    cost_per_unit = models.DecimalField(max_digits=12, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    tax_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    customs_fee_share = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    import_fee_share = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    logistics_expense_share = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    final_cost = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.asset.name} (x{self.quantity})"

    @property
    def total_cost(self):
        return self.quantity * self.cost_per_unit




class FixedAssetsPurchaseInvoice(models.Model):
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

    purchase_order = models.ForeignKey(FixedAssetsPurchase, on_delete=models.CASCADE, related_name="invoices",
                                       verbose_name=_("Purchase Order"))
    invoice_number = models.CharField(max_length=20, verbose_name=_("Invoice Number"))
    supplier = models.ForeignKey("purchase.Vendor", on_delete=models.CASCADE, related_name='fixed_assets_purchase_invoices',
                                 verbose_name=_("Supplier"))
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE,
                                     related_name='fixed_assets_purchase_invoices', verbose_name=_("Organization"))
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

    def save(self, *args, **kwargs):
        # Automatically calculate the remaining balance
        self.remaining_balance = self.total_amount - self.paid_amount
        if self.remaining_balance > 0 and self.paid_amount > 0:
            self.status = self.STATUS_PARTIALLY_PAID
        elif self.remaining_balance == 0:
            self.status = self.STATUS_PAID
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Fixed Assets Purchase Invoice {self.id} - {self.supplier}"



