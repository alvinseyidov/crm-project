from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Tax(models.Model):
    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE,
        related_name="taxes"
    )
    name = models.CharField(max_length=256)
    percent = models.DecimalField(max_digits=6, decimal_places=3)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.organization.name} - {self.name} - {self.percent}%'



class BankAccount(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('RUB', 'Russian Ruble'),
        ('AZN', 'Azerbaijani Manat'),
        ('TL', 'Turkish Lira'),
    ]

    account_number = models.CharField(max_length=50, unique=True, verbose_name=_("Account Number"))
    bank_name = models.CharField(max_length=100, verbose_name=_("Bank Name"))
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD', verbose_name=_("Currency"))
    balance = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_("Balance"))
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE, related_name='bank_accounts',
                                     verbose_name=_("Organization"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Bank Account")
        verbose_name_plural = _("Bank Accounts")

    def __str__(self):
        return f"{self.bank_name} - {self.account_number}"


class TaxDepositAccount(models.Model):
    CURRENCY_CHOICES = [
        ('AZN', 'Azerbaijani Manat'),
    ]

    account_number = models.CharField(max_length=50, unique=True, verbose_name=_("Account Number"))
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='AZN', verbose_name=_("Currency"))
    balance = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_("Balance"))
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE, related_name='tax_deposit_accounts',
                                     verbose_name=_("Organization"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Tax Deposit Account")
        verbose_name_plural = _("Tax Deposit Accounts")

    def __str__(self):
        return f"VAT {self.organization.name}% - {self.account_number}"



from django.db import models
from django.utils.translation import gettext_lazy as _

class CashAccount(models.Model):
    CURRENCY_CHOICES = [
        ('AZN', 'Azerbaijani Manat'),
    ]

    ACCOUNT_TYPE_CHOICES = [
        ('TREASURY', 'Treasury Account'),
        ('SUB', 'Sub Cash Account'),
    ]

    account_name = models.CharField(max_length=100, unique=True, verbose_name=_("Account Name"))
    account_type = models.CharField(max_length=8, choices=ACCOUNT_TYPE_CHOICES, default='SUB', verbose_name=_("Account Type"))
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='AZN', verbose_name=_("Currency"))
    balance = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_("Balance"))
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE, related_name='cash_accounts', verbose_name=_("Organization"))
    responsible_person = models.ForeignKey('hr.Worker', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Responsible Person"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Cash Account")
        verbose_name_plural = _("Cash Accounts")

    def __str__(self):
        return f"{self.account_type} - {self.account_name}"







class SalesInvoicePayment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('BANK', 'Bank Account'),
        ('CASH', 'Cash Account'),
    ]
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE,
                                     related_name='sales_invoice_payments', verbose_name=_("Organization"))
    sales_invoice = models.ForeignKey('sale.SalesInvoice', on_delete=models.CASCADE, related_name='payments', verbose_name=_("Sales Invoice"))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Payment Amount"))
    payment_method = models.CharField(max_length=4, choices=PAYMENT_METHOD_CHOICES, verbose_name=_("Payment Method"))
    bank_account = models.ForeignKey('BankAccount', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Bank Account"))
    cash_account = models.ForeignKey('CashAccount', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Cash Account"))
    payment_date = models.DateField(verbose_name=_("Payment Date"))
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))

    def save(self, *args, **kwargs):
        # Update the related invoice's paid amount and status
        self.sales_invoice.paid_amount += self.amount
        self.sales_invoice.save()

        # Update the bank or cash account balance
        if self.payment_method == 'BANK' and self.bank_account:
            self.bank_account.balance -= self.amount
            self.bank_account.save()
        elif self.payment_method == 'CASH' and self.cash_account:
            self.cash_account.balance -= self.amount
            self.cash_account.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Sales Payment {self.id} - {self.amount}"





class PurchaseBillPayment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('BANK', 'Bank Account'),
        ('CASH', 'Cash Account'),
    ]
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE,
                                     related_name='purchase_bill_payments', verbose_name=_("Organization"))
    purchase_bill = models.ForeignKey('purchase.Bill', on_delete=models.CASCADE, related_name='bill_payments', verbose_name=_("Purchase Bill"))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Payment Amount"))
    payment_method = models.CharField(max_length=4, choices=PAYMENT_METHOD_CHOICES, verbose_name=_("Payment Method"))
    bank_account = models.ForeignKey('BankAccount', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Bank Account"))
    cash_account = models.ForeignKey('CashAccount', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Cash Account"))
    payment_date = models.DateField(verbose_name=_("Payment Date"))
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))

    def save(self, *args, **kwargs):


        # Update the bank or cash account balance
        if self.payment_method == 'BANK' and self.bank_account:
            self.bank_account.balance -= self.amount
            self.bank_account.save()
        elif self.payment_method == 'CASH' and self.cash_account:
            self.cash_account.balance -= self.amount
            self.cash_account.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Purchase Payment {self.id} - {self.amount}"


class FixedAssetsPurchaseInvoicePayment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('BANK', 'Bank Account'),
        ('CASH', 'Cash Account'),
    ]
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE,
                                     related_name='fixed_assets_purchase_invoice_payments', verbose_name=_("Organization"))
    fixed_assets_purchase_invoice = models.ForeignKey('assets.FixedAssetsPurchaseInvoice', on_delete=models.CASCADE, related_name='payments', verbose_name=_("Fixed Assets Purchase Invoice"))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Payment Amount"))
    payment_method = models.CharField(max_length=4, choices=PAYMENT_METHOD_CHOICES, verbose_name=_("Payment Method"))
    bank_account = models.ForeignKey('BankAccount', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Bank Account"))
    cash_account = models.ForeignKey('CashAccount', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Cash Account"))
    payment_date = models.DateField(verbose_name=_("Payment Date"))
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))

    def save(self, *args, **kwargs):
        # Update the related invoice's paid amount and status
        self.fixed_assets_purchase_invoice.paid_amount += self.amount
        self.fixed_assets_purchase_invoice.save()

        # Update the bank or cash account balance
        if self.payment_method == 'BANK' and self.bank_account:
            self.bank_account.balance -= self.amount
            self.bank_account.save()
        elif self.payment_method == 'CASH' and self.cash_account:
            self.cash_account.balance -= self.amount
            self.cash_account.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Purchase Payment {self.id} - {self.amount}"




class ExpensePayment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('BANK', 'Bank Account'),
        ('CASH', 'Cash Account'),
    ]

    expense = models.ForeignKey('expense.Expense', on_delete=models.CASCADE, related_name='payments', verbose_name=_("Expense"))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Payment Amount"))
    payment_method = models.CharField(max_length=4, choices=PAYMENT_METHOD_CHOICES, verbose_name=_("Payment Method"))
    bank_account = models.ForeignKey('BankAccount', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Bank Account"))
    cash_account = models.ForeignKey('CashAccount', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Cash Account"))
    payment_date = models.DateField(verbose_name=_("Payment Date"))
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))

    def save(self, *args, **kwargs):
        # No need to update anything like in invoice cases, just reduce the cash or bank account balance
        if self.payment_method == 'BANK' and self.bank_account:
            self.bank_account.balance -= self.amount
            self.bank_account.save()
        elif self.payment_method == 'CASH' and self.cash_account:
            self.cash_account.balance -= self.amount
            self.cash_account.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Expense Payment {self.id} - {self.amount}"




