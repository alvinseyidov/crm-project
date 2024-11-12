from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product
from inventory.models import Stock, Warehouse  # Import Stock and Warehouse models


@receiver(post_save, sender=Product)
def create_stock_for_new_product(sender, instance, created, **kwargs):
    """Create a Stock record for each new product in the organization's warehouses."""
    if created:
        # Check if there are any warehouses for the product's organization
        warehouses = Warehouse.objects.filter(organization=instance.organization)

        # If no warehouse exists, create a default 'Main Warehouse'
        if not warehouses.exists():
            main_warehouse = Warehouse.objects.create(name="Main Warehouse", organization=instance.organization)
            warehouses = [main_warehouse]  # Treat the new warehouse as the only warehouse

        # Create stock entries for the product in all the warehouses
        for warehouse in warehouses:
            Stock.objects.create(product=instance, warehouse=warehouse, quantity=0)



