from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _



class SalesOrder(models.Model):
    INVENTORY_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('canceled', 'Canceled'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('invoiced', 'Invoiced'),
        ('paid', 'Paid'),
        ('partial_paid', 'Partial Paid'),
    ]
    
    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE
    )
    customer = models.ForeignKey(
        'customer.Customer',
        on_delete=models.CASCADE
    )
    warehouse = models.ForeignKey(
        'inventory.Warehouse',
        on_delete=models.CASCADE,
        related_name='warehouse_sales'
    )
    order_number = models.CharField(max_length=255, unique=True)
    salesperson = models.ForeignKey('hr.Worker', on_delete=models.SET_NULL, null=True, verbose_name=_("Salesperson"))
    date = models.DateField()
    delivery_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=INVENTORY_STATUS_CHOICES, default='draft')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='invoiced')
    description = models.TextField(blank=True, null=True)

    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, default=0.0)
    grand_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return f"{self.order_number} ({self.customer.name})"


class SalesOrderItem(models.Model):
    sales_order = models.ForeignKey('SalesOrder', on_delete=models.CASCADE, related_name='sales_order_items')
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE, related_name='sales_order_items')
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    price_per_unit = models.DecimalField(max_digits=12, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    tax = models.ForeignKey('accounting.Tax', on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.price_per_unit
        if self.discount_percentage:
            self.total_price *= (1 - self.discount_percentage / 100)
        if self.tax:
            self.tax_amount = self.total_price * (self.tax.percent / 100)
        else:
            self.tax_amount = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"



class SalesReturnOrder(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('processed', 'Processed'),
        ('canceled', 'Canceled'),
    ]

    sales_order = models.ForeignKey(SalesOrder, on_delete=models.SET_NULL, null=True, blank=True, related_name='return_orders')
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
        # Generate return number with sales order number or organization
        last_return = SalesReturnOrder.objects.filter(sales_order=self.sales_order).order_by('id').last()

        if last_return:
            last_return_number = last_return.return_number.split('-')[-1]  # Get the numeric part
            return_int = int(last_return_number[1:])  # Remove 'R' and convert to int
            new_return_number = f'R{return_int + 1:06d}'  # Increment and format
        else:
            new_return_number = 'R000001'  # Start with R000001
        # Prefix with sales order number
        self.return_number = f'{self.sales_order.order_number}-{new_return_number}'  # Example: SO-000001-R000001
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.return_number} (SalesOrder: {self.sales_order.order_number})"




class SalesReturnOrderItem(models.Model):
    return_order = models.ForeignKey('SalesReturnOrder', on_delete=models.CASCADE, related_name='return_order_items')
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    price_per_unit = models.DecimalField(max_digits=12, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    tax = models.ForeignKey('accounting.Tax', on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.price_per_unit
        if self.discount_percentage:
            self.total_price *= (1 - self.discount_percentage / 100)
        if self.tax:
            self.tax_amount = self.total_price * (self.tax.percent / 100)
        else:
            self.tax_amount = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Return {self.product.name} ({self.quantity})"


from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class SalesInvoice(models.Model):
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
    sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name="invoices",
                                    verbose_name=_("Sales Order"))
    invoice_number = models.CharField(max_length=20, verbose_name=_("Invoice Number"))

    customer = models.ForeignKey("customer.Customer", on_delete=models.CASCADE, related_name='sales_invoices',
                                 verbose_name=_("Customer"))
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE,
                                     related_name='sales_invoices', verbose_name=_("Organization"))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Total Amount"))
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name=_("Paid Amount"))
    remaining_balance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Remaining Balance"))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT, verbose_name=_("Status"))
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
        return f"Invoice {self.id} - {self.customer}"

