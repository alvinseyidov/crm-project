from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class ExpenseCategory(models.Model):
    organization = models.ForeignKey("organization.Organization", on_delete=models.CASCADE, related_name='expense_categories')
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('organization', 'name')

    def __str__(self):
        return self.name

def validate_receipt_size(value):
    limit = 2 * 1024 * 1024  # 2 MB
    if value.size > limit:
        raise ValidationError('Receipt size should not exceed 2 MB.')




class Expense(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
        ('paid', 'Paid'),
    ]
    EXPENSE_TYPE_CHOICES = [
        ('operational', 'Operational'),
        ('administrative', 'Administrative'),
        ('purchase_related', 'Purchase Related'),
        ('sales_related', 'Sales Related'),
        ('other', 'Other'),
    ]
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('RUB', 'Russian Ruble'),
        ('AZN', 'Azerbaijani Manat'),
        ('TL', 'Turkish Lira'),
    ]
    organization = models.ForeignKey("organization.Organization", on_delete=models.CASCADE, related_name='expenses')
    expense_type = models.CharField(max_length=20, choices=EXPENSE_TYPE_CHOICES, default='other',
                                   verbose_name=_("Expense Type"))
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='AZN', verbose_name=_("Currency"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="expenses")
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE, related_name="expenses")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    receipt = models.ImageField(upload_to='receipts/', null=True, blank=True, validators=[validate_receipt_size])
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')

    purchase = models.ForeignKey('purchase.Purchase', on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='expenses', verbose_name=_("Related Purchase"))
    sales_order = models.ForeignKey('sale.SalesOrder', on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='expenses', verbose_name=_("Related Sales Order"))

    submitted_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    rejected_at = models.DateTimeField(null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)



    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('date',)
    def clean(self):
        if self.amount <= 0:
            raise ValidationError('Expense amount must be greater than zero.')



    def __str__(self):
        return f"{self.category.name} - {self.amount}"