from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import PurchaseBillPayment



@receiver(post_save, sender=PurchaseBillPayment)
def update_bill_status_on_payment(sender, instance, created, **kwargs):
    """Update Bill status when a payment is made."""
    if created:
        bill = instance.purchase_bill
        bill.paid_amount += instance.amount
        bill.remaining_balance = max(bill.total_amount - bill.paid_amount, 0)

        if bill.remaining_balance == 0:
            bill.status = 'paid'
        elif bill.paid_amount > 0:
            bill.status = 'partially_paid'

        bill.save()



@receiver(post_delete, sender=PurchaseBillPayment)
def reverse_bill_status_on_payment_delete(sender, instance, **kwargs):
    """Reverse update Bill status when a payment is deleted."""
    bill = instance.purchase_bill
    bill.paid_amount -= instance.amount
    bill.remaining_balance = max(bill.total_amount - bill.paid_amount, 0)

    if bill.paid_amount == 0:
        bill.status = 'issued'
    elif bill.remaining_balance == 0:
        bill.status = 'paid'
    else:
        bill.status = 'partially_paid'

    # Ensure paid_amount and remaining_balance do not go negative
    bill.paid_amount = max(bill.paid_amount, 0)
    bill.remaining_balance = max(bill.remaining_balance, 0)

    bill.save()