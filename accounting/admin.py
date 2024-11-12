from django.contrib import admin
from .models import *

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ['organization','name','percent','description']


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'bank_name', 'currency', 'balance', 'organization', 'created_at', 'updated_at')
    list_filter = ('currency', 'bank_name', 'organization')
    search_fields = ('account_number', 'bank_name', 'organization__name')
    readonly_fields = ('created_at', 'updated_at')



@admin.register(TaxDepositAccount)
class TaxDepositAccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'currency', 'balance', 'organization', 'created_at', 'updated_at')
    list_filter = ('organization', 'currency')
    search_fields = ('account_number', 'organization__name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(CashAccount)
class CashAccountAdmin(admin.ModelAdmin):
    list_display = ('account_name', 'account_type', 'currency', 'balance', 'organization', 'responsible_person', 'created_at', 'updated_at')
    list_filter = ('account_type', 'organization', 'responsible_person')
    search_fields = ('account_name', 'organization__name', 'responsible_person__username')
    readonly_fields = ('created_at', 'updated_at')



@admin.register(SalesInvoicePayment)
class SalesInvoicePaymentAdmin(admin.ModelAdmin):
    list_display = ('sales_invoice', 'amount', 'payment_method', 'bank_account', 'cash_account', 'payment_date')
    list_filter = ('payment_method', 'bank_account', 'cash_account')
    search_fields = ('sales_invoice__invoice_number', 'bank_account__account_name', 'cash_account__account_name')
    readonly_fields = ('payment_date',)

@admin.register(PurchaseBillPayment)
class PurchaseBillPaymentAdmin(admin.ModelAdmin):
    list_display = ('purchase_bill', 'amount', 'payment_method', 'bank_account', 'cash_account', 'payment_date')
    list_filter = ('payment_method', 'bank_account', 'cash_account')
    search_fields = ('purchase_bill__bill_number', 'bank_account__account_name', 'cash_account__account_name')


@admin.register(FixedAssetsPurchaseInvoicePayment)
class FixedAssetsPurchaseInvoicePaymentAdmin(admin.ModelAdmin):
    list_display = ('fixed_assets_purchase_invoice', 'amount', 'payment_method', 'bank_account', 'cash_account', 'payment_date')
    list_filter = ('payment_method', 'bank_account', 'cash_account')
    search_fields = ('purchase_invoice__invoice_number', 'bank_account__account_name', 'cash_account__account_name')
    readonly_fields = ('payment_date',)


@admin.register(ExpensePayment)
class ExpensePaymentAdmin(admin.ModelAdmin):
    list_display = ('expense', 'amount', 'payment_method', 'bank_account', 'cash_account', 'payment_date')
    list_filter = ('payment_method', 'bank_account', 'cash_account')
    search_fields = ('expense__category__name', 'bank_account__account_name', 'cash_account__account_name')
    readonly_fields = ('payment_date',)


