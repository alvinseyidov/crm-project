from django.contrib import admin
from .models import *



@admin.register(FixedAssetsCategory)
class FixedAssetsCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'description')
    search_fields = ('name', 'organization__name')
    list_filter = ('organization',)


@admin.register(FixedAssets)
class FixedAssetsAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'asset_category', 'purchase_date', 'purchase_price', 'depreciation_rate', 'serial_number')
    search_fields = ('name', 'serial_number', 'organization__name', 'asset_category__name')
    list_filter = ('organization', 'asset_category', 'purchase_date')
    readonly_fields = ('purchase_date',)




class FixedAssetsPurchaseItemInline(admin.TabularInline):
    model = FixedAssetsPurchaseItem
    extra = 1  # This controls how many empty inlines appear for new items
    readonly_fields = ('total_price', 'final_cost')

@admin.register(FixedAssetsPurchase)
class FixedAssetsPurchaseAdmin(admin.ModelAdmin):
    list_display = (
        'organization',
        'vendor',
        'purchase_date',
        'total_cost',
        'tax_amount',
        'grand_total',
        'payment_status',
        'currency',
        'currency_rate',
        'customs_fee',
        'import_fee',
        'logistic_expenses',
        'ygb_number',
        'ygb_payment',
        'created_at',
        'updated_at'
    )
    search_fields = ('organization__name', 'vendor__name', 'ygb_number')
    list_filter = ('organization', 'vendor', 'purchase_date', 'payment_status', 'currency')
    inlines = [FixedAssetsPurchaseItemInline]
    readonly_fields = ('created_at', 'updated_at')  # Optional to make these fields read-only in the admin


@admin.register(FixedAssetsPurchaseInvoice)
class FixedAssetsPurchaseInvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'purchase_order', 'supplier', 'organization', 'total_amount', 'paid_amount', 'remaining_balance', 'status', 'issued_date', 'due_date', 'created_at')
    list_filter = ('status', 'supplier', 'organization', 'issued_date', 'due_date')
    search_fields = ('invoice_number', 'supplier__name', 'organization__name', 'purchase_order__order_number')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'issued_date'