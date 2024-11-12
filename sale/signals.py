from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import SalesOrder, SalesOrderItem, SalesReturnOrder
from inventory.models import Stock, StockMovement

# Dictionary to store the previous state of SalesOrder
previous_sales_status_cache = {}

@receiver(pre_save, sender=SalesOrder)
def cache_previous_sales_status(sender, instance, **kwargs):
    """
    Cache the previous status of the SalesOrder instance before saving.
    """
    if instance.pk:
        try:
            previous_instance = SalesOrder.objects.get(pk=instance.pk)
            previous_sales_status_cache[instance.pk] = previous_instance.status
        except SalesOrder.DoesNotExist:
            previous_sales_status_cache[instance.pk] = None

@receiver(post_save, sender=SalesOrder)
def handle_sales_order_status_change(sender, instance, **kwargs):
    """
    Signal to handle stock updates and stock movements when SalesOrder status changes.
    """
    previous_status = previous_sales_status_cache.get(instance.pk, None)
    new_status = instance.status

    # Remove from cache after post_save to prevent stale data
    if instance.pk in previous_sales_status_cache:
        del previous_sales_status_cache[instance.pk]

    # Only process when status changes
    if previous_status != new_status:
        # Now we loop through sales items safely after the sales order and items are saved
        for item in instance.sales_order_items.all():
            # Find related stock record
            stock, created = Stock.objects.get_or_create(product=item.product, warehouse=instance.warehouse)

            # Handle status transitions
            if new_status == 'confirmed':
                # When status is 'confirmed', reserve the stock without physically removing it
                stock.reserved_quantity += item.quantity
                stock.save()

                # Log the stock movement for reserved stock
                StockMovement.objects.create(
                    product=item.product,
                    warehouse=instance.warehouse,
                    quantity=item.quantity,
                    movement_type='RESERVED',  # Log reserved stock
                    sales_order=instance
                )

            elif new_status == 'shipped':
                # When status is 'shipped', decrease reserved_quantity and actual stock, log stock movement
                stock.quantity -= item.quantity  # Physically decrease stock
                stock.reserved_quantity -= min(stock.reserved_quantity, item.quantity)  # Release reserved stock
                stock.save()

                # Log the stock movement for shipped sales order
                StockMovement.objects.create(
                    product=item.product,
                    warehouse=instance.warehouse,
                    quantity=-item.quantity,  # Outgoing stock for sales
                    movement_type='OUT',
                    sales_order=instance
                )

            elif new_status == 'canceled':
                # If the order is canceled, reverse the reserved stock or stock that was shipped
                if previous_status == 'confirmed':
                    # If the order was confirmed but not shipped, release reserved stock
                    stock.reserved_quantity -= min(stock.reserved_quantity, item.quantity)
                    stock.save()

                    # Log the reversal of reserved stock
                    StockMovement.objects.create(
                        product=item.product,
                        warehouse=instance.warehouse,
                        quantity=-item.quantity,  # Reversing the reserved stock
                        movement_type='RESERVED',  # Reversing reserved stock
                        sales_order=instance
                    )

                elif previous_status == 'shipped':
                    # If the order was shipped, reverse the physical stock removal
                    stock.quantity += item.quantity  # Return the stock to warehouse
                    stock.save()

                    # Log the reversal movement
                    StockMovement.objects.create(
                        product=item.product,
                        warehouse=instance.warehouse,
                        quantity=item.quantity,  # Returning stock
                        movement_type='CANCELLED_SALE',  # Stock is coming back due to cancellation
                        sales_order=instance
                    )