from django.db.models.signals import post_save, pre_delete, pre_save, post_delete
from django.dispatch import receiver
from .models import Purchase, PurchaseReceive, PurchaseReceiveItem, Bill, PurchaseItem, LandedCost
from inventory.models import Stock, StockMovement


old_status_cache = {}


@receiver(pre_save, sender=Purchase)
def capture_old_status(sender, instance, **kwargs):
    """Signal to capture the old status of the Purchase before saving."""
    if instance.pk:
        try:
            old_status_cache[instance.pk] = sender.objects.get(pk=instance.pk).status
        except sender.DoesNotExist:
            old_status_cache[instance.pk] = None









@receiver(post_save, sender=Purchase)
def create_or_update_stock_movement(sender, instance, created, **kwargs):
    """Signal to create or update stock movement based on Purchase status."""
    old_status = old_status_cache.get(instance.pk, None)

    # Clear the cache after use to avoid memory buildup
    if instance.pk in old_status_cache:
        del old_status_cache[instance.pk]

    if old_status != instance.status:
        for item in instance.items.all():
            warehouse = instance.organization.warehouses.first()  # Adjust as needed

            if instance.status in ['confirmed', 'shipped'] and old_status not in ['confirmed', 'shipped']:
                # Create 'EXPECTED' stock movement
                StockMovement.objects.create(
                    product=item.product,
                    warehouse=warehouse,
                    quantity=item.quantity,
                    movement_type='EXPECTED',
                    purchase_order=instance
                )
                if not instance.bills.exists():
                    bill = Bill.objects.get_or_create(
                        purchase=instance,
                        defaults={
                            'bill_number': f"BO-{instance.id:06}",  # Generate a unique bill number (adjust as needed)
                            'supplier': instance.vendor,
                            'organization': instance.organization,
                            'total_amount': instance.total_cost,
                            'remaining_balance': instance.total_cost,
                            'paid_amount': 0,
                            'issued_date': instance.date,
                            'status': 'issued',
                        }
                    )






@receiver(post_save, sender=Purchase)
def handle_status_change_and_create_receive(sender, instance, created, **kwargs):
    """Signal to handle purchase status change to 'received' and create PurchaseReceive."""
    old_status = old_status_cache.get(instance.pk, None)

    # Clear the cache after use to avoid memory buildup
    if instance.pk in old_status_cache:
        del old_status_cache[instance.pk]

    if old_status != instance.status:
        warehouse = instance.organization.warehouses.first()  # Adjust as needed

        if instance.status == 'received' and old_status not in ['received']:
            # Create a PurchaseReceive when the status changes to 'received'
            purchase_receive, createdp = PurchaseReceive.objects.get_or_create(
                organization=instance.organization,
                purchase=instance,
                status='received',
            )
            print("--------")
            print(createdp)
            if createdp:
                # Create PurchaseReceiveItems for each PurchaseItem
                for item in instance.items.all():
                    PurchaseReceiveItem.objects.create(
                        purchase_receive=purchase_receive,
                        product=item.product,
                        ordered_quantity=item.quantity,
                        received_quantity=item.quantity,  # Assuming full receipt
                        is_fully_received=True,
                    )

            if not instance.bills.exists():
                bill = Bill.objects.get_or_create(
                    purchase=instance,
                    defaults={
                        'bill_number': f"BO-{instance.id:06}",  # Generate a unique bill number (adjust as needed)
                        'supplier': instance.vendor,
                        'organization': instance.organization,
                        'total_amount': instance.total_cost,
                        'remaining_balance': instance.total_cost,
                        'paid_amount': 0,
                        'issued_date': instance.date,
                        'status': 'issued',
                    }
                )


@receiver(post_save, sender=PurchaseReceiveItem)
def handle_purchase_receive(sender, instance, created, **kwargs):
    """Signal to create stock movement and update stock when PurchaseReceive is created."""
    if created:
        # Create stock movement
        StockMovement.objects.create(
            product=instance.product,
            warehouse=instance.purchase_receive.warehouse,
            quantity=instance.received_quantity,
            movement_type='IN',
            purchase_receive=instance.purchase_receive,
            stock_batch=None  # Adjust if needed
        )
        expected_stock_movement = StockMovement.objects.filter(
            product=instance.product,
            warehouse=instance.purchase_receive.warehouse,
            movement_type='EXPECTED',
            purchase_order=instance.purchase_receive.purchase,
        )
        expected_stock_movement.delete()


@receiver(post_save, sender=PurchaseReceive)
def handle_purchase_receive(sender, instance, created, **kwargs):
    """Signal to create stock movement and update stock when PurchaseReceive is created."""
    if created:
        # Create stock movement
        if instance.purchase.status != 'received':
            instance.purchase.status = 'received'
            instance.purchase.save()

@receiver(post_save, sender=PurchaseItem)
def handle_purchase_item_creation(sender, instance, created, **kwargs):
    """Signal to create stock movement and update stock when PurchaseReceive is created."""
    if created:
        instance.purchase.save()

@receiver(post_save, sender=LandedCost)
def handle_purchase_item_creation(sender, instance, created, **kwargs):
    """Signal to create stock movement and update stock when PurchaseReceive is created."""
    if created:
        instance.purchase.save()