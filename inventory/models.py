from django.db import models
from django.conf import settings

from catalog.models import Product


class Warehouse(models.Model):
    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE,
        related_name="warehouses"
    )
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.name



class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    reserved_quantity = models.PositiveIntegerField(default=0)  # For pending orders
    expected_quantity = models.PositiveIntegerField(default=0)  # For shipped purchases not yet received
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def available_stock(self):
        return self.quantity - self.reserved_quantity

    def increase_stock(self, amount, movement_type='IN', related_order=None):
        """Increase stock and log a stock movement."""

        # Log the stock movement
        StockMovement.objects.create(
            product=self.product,
            warehouse=self.warehouse,
            quantity=amount,
            movement_type=movement_type,  # 'IN' for incoming stock
            stock_batch=None,  # You can adjust this to link to a StockBatch if applicable
            purchase_order=related_order if movement_type == 'IN' else None,
        )


    def decrease_stock(self, amount, movement_type='OUT', related_order=None):
        """Decrease stock and log a stock movement."""


        # Log the stock movement
        StockMovement.objects.create(
            product=self.product,
            warehouse=self.warehouse,
            quantity=-amount,  # Store as negative for 'OUT' movements
            movement_type=movement_type,  # 'OUT' for outgoing stock
            sales_order=related_order if movement_type == 'OUT' else None,
            purchase_return_order=related_order if movement_type == 'OUT' else None
        )


    def __str__(self):
        return f"{self.product.name} - {self.warehouse.name}"


class StockBatch(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    received_date = models.DateTimeField(auto_now_add=True)
    remaining_quantity = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} units"

class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('IN', 'Stock In'),  # Actual incoming stock, such as purchases, returns
        ('OUT', 'Stock Out'),  # Actual outgoing stock, such as sales, adjustments
        ('TRANSFER', 'Transfer'),  # Stock transfer between warehouses
        ('EXPECTED', 'Expected Stock'),  # Expected incoming stock
        ('RESERVED', 'Reserved Stock'),  # Reserved incoming stock (e.g., reserved for pending orders)
        ('CANCELLED_PURCHASE', 'Cancelled Purchase'),  # Stock adjustment for cancelled purchases
        ('CANCELLED_SALE', 'Cancelled Sale'),  # Stock adjustment for cancelled sales
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    quantity = models.IntegerField()  # Positive for stock in, negative for stock out
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    source_warehouse = models.ForeignKey(
        Warehouse, null=True, blank=True, related_name='source_warehouse', on_delete=models.SET_NULL
    )
    destination_warehouse = models.ForeignKey(
        Warehouse, null=True, blank=True, related_name='destination_warehouse', on_delete=models.SET_NULL
    )

    # Link to sales-related orders
    purchase_order = models.ForeignKey("purchase.Purchase", null=True, blank=True, on_delete=models.CASCADE)
    purchase_receive = models.ForeignKey("purchase.PurchaseReceive", null=True, blank=True, on_delete=models.CASCADE)
    sales_order = models.ForeignKey("sale.SalesOrder", null=True, blank=True, on_delete=models.SET_NULL)

    # New fields for handling returns
    sales_return_order = models.ForeignKey("sale.SalesReturnOrder", null=True, blank=True, on_delete=models.SET_NULL)
    purchase_return_order = models.ForeignKey("purchase.PurchaseReturn", null=True, blank=True, on_delete=models.SET_NULL)

    movement_date = models.DateTimeField(auto_now_add=True)

    stock_batch = models.ForeignKey(StockBatch, null=True, blank=True, on_delete=models.SET_NULL)

    def create_movement(self, product, warehouse, quantity, movement_type):
        # Deduct stock from the batch in FIFO order
        batches = StockBatch.objects.filter(product=product, warehouse=warehouse).order_by('received_date')
        for batch in batches:
            if quantity <= batch.quantity:
                batch.quantity -= quantity
                StockMovement.objects.create(
                    product=product,
                    warehouse=warehouse,
                    quantity=quantity,
                    movement_type=movement_type,
                    stock_batch=batch
                )
                batch.save()
                break
            else:
                movement_quantity = batch.quantity
                batch.quantity = 0
                StockMovement.objects.create(
                    product=product,
                    warehouse=warehouse,
                    quantity=movement_quantity,
                    movement_type=movement_type,
                    stock_batch=batch
                )
                quantity -= movement_quantity
                batch.save()

    def __str__(self):
        return f"{self.movement_type} - {self.product.name} - {self.quantity}"

    def is_return_movement(self):
        """Helper method to identify if the stock movement is related to a return."""
        return self.sales_return_order is not None or self.purchase_return_order is not None






class StockAdjustment(models.Model):
    ADJUSTMENT_TYPES = [
        ('RETURN', 'Return'),
        ('DAMAGE', 'Damage'),
        ('EXCESS', 'Excess'),
        ('SHORTAGE', 'Shortage'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    quantity = models.IntegerField()  # Positive for excess, negative for shortage/damage
    adjustment_type = models.CharField(max_length=20, choices=ADJUSTMENT_TYPES)
    reason = models.TextField(null=True, blank=True)
    adjusted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.adjustment_type} - {self.product.name} - {self.quantity}"
