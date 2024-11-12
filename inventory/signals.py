from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Stock, StockMovement

@receiver(post_save, sender=StockMovement)
def adjust_stock_based_on_movement(sender, instance, created, **kwargs):
    """Signal to adjust stock based on the stock movement."""
    if created:
        stock, _ = Stock.objects.get_or_create(
            product=instance.product,
            warehouse=instance.warehouse
        )

        if instance.movement_type == 'IN':
            stock.quantity += instance.quantity
        elif instance.movement_type == 'OUT':
            stock.quantity -= abs(instance.quantity)  # Ensure subtraction
        elif instance.movement_type == 'EXPECTED':
            stock.expected_quantity += instance.quantity
        elif instance.movement_type == 'RESERVED':
            stock.reserved_quantity += instance.quantity



        # Ensure stock and expected/reserved quantities are non-negative
        stock.quantity = max(stock.quantity, 0)
        stock.expected_quantity = max(stock.expected_quantity, 0)
        stock.reserved_quantity = max(stock.reserved_quantity, 0)
        stock.save()

@receiver(post_delete, sender=StockMovement)
def adjust_stock_on_movement_delete(sender, instance, **kwargs):
    """Signal to adjust stock when a StockMovement is deleted."""
    try:
        stock = Stock.objects.get(product=instance.product, warehouse=instance.warehouse)

        # Adjust stock based on the type of movement
        if instance.movement_type == 'IN':
            stock.quantity -= instance.quantity  # Reduce the stock quantity
        elif instance.movement_type == 'OUT':
            stock.quantity += abs(instance.quantity)  # Increase the stock quantity
        elif instance.movement_type == 'EXPECTED':
            stock.expected_quantity -= instance.quantity  # Reduce the expected quantity
        elif instance.movement_type == 'RESERVED':
            stock.reserved_quantity -= instance.quantity  # Reduce reserved quantity



        # Ensure the quantities don't go negative
        stock.quantity = max(stock.quantity, 0)
        stock.expected_quantity = max(stock.expected_quantity, 0)
        stock.reserved_quantity = max(stock.reserved_quantity, 0)

        stock.save()

    except Stock.DoesNotExist:
        # If the Stock record does not exist, skip adjustment
        pass
