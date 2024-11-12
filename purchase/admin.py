from django.contrib import admin
from .models import Vendor, Purchase, PurchaseItem, PurchaseReturn, PurchaseReturnItem, LandedCost, \
    PurchaseReceive, PurchaseReceiveItem, Bill, PurchaseDocument


# Admin configuration for Vendor
@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'contact_person', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active','organization', 'country','created_at', 'updated_at')
    search_fields = ('name', 'email', 'phone', 'contact_person')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')



class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1
    fields = (
        'product', 'quantity', 'unit_cost', 'item_total_cost', 'discount_amount',
        'allocated_landed_cost','vat_applicable_cost', 'tax', 'tax_amount', 'grand_total', 'weight', 'volume',
    )
    readonly_fields = ('item_total_cost', 'tax_amount', 'grand_total')
    autocomplete_fields = ['product']
    verbose_name_plural = "Purchase Items"

class LandedCostInline(admin.TabularInline):
    model = LandedCost
    extra = 1
    fields = ('cost_type', 'amount', 'organization')
    autocomplete_fields = ['organization']
    verbose_name_plural = "Landed Costs"

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        'order_number', 'vendor', 'organization', 'purchase_type', 'purchase_origin',
        'status', 'currency', 'total_amount', 'tax_amount', 'grand_total',
        'date', 'expected_delivery_date'
    )
    list_filter = ('status', 'purchase_origin', 'purchase_type', 'currency')
    search_fields = ('order_number', 'vendor__name', 'organization__name')
    readonly_fields = ('total_amount', 'tax_amount', 'grand_total')
    date_hierarchy = 'date'
    inlines = []

    def get_inlines(self, request, obj=None):
        # Adds PurchaseItemInline and LandedCostInline if a purchase is being viewed
        if obj:
            self.inlines = [PurchaseItemInline, LandedCostInline]
        return super().get_inlines(request, obj)


@admin.register(LandedCost)
class LandedCostAdmin(admin.ModelAdmin):
    list_display = ('cost_type', 'amount', 'purchase', 'organization', 'created_at')
    list_filter = ('cost_type', 'organization')
    search_fields = ('purchase__order_number', 'organization__name', 'description')
    readonly_fields = ('created_at', 'updated_at')


class PurchaseReceiveItemInline(admin.TabularInline):
    model = PurchaseReceiveItem
    extra = 1  # Allows adding additional empty rows for new items
    readonly_fields = ('is_fully_received',)
    fields = ('product', 'ordered_quantity', 'received_quantity', 'is_fully_received')

    def has_add_permission(self, request, obj=None):
        # Prevent adding new items directly from the inline if not needed
        return True


@admin.register(PurchaseDocument)
class PurchaseDocumentAdmin(admin.ModelAdmin):
    list_display = ('purchase', 'description', 'uploaded_at')
    search_fields = ('purchase__id', 'description')

@admin.register(PurchaseReceive)
class PurchaseReceiveAdmin(admin.ModelAdmin):
    list_display = ('purchase', 'receive_date', 'status', 'total_received_quantity', 'remarks')
    list_filter = ('status', 'receive_date', 'purchase__vendor')
    search_fields = ('purchase__order_number', 'purchase__vendor__name')
    readonly_fields = ('receive_date', 'total_received_quantity')
    inlines = [PurchaseReceiveItemInline]


# Inline for PurchaseReturnItem, to manage items within the PurchaseReturn admin page
class PurchaseReturnItemInline(admin.TabularInline):
    model = PurchaseReturnItem
    extra = 1  # Number of empty slots for new items

# Admin for PurchaseReturn
@admin.register(PurchaseReturn)
class PurchaseReturnAdmin(admin.ModelAdmin):
    list_display = ['return_number', 'purchase_order', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'purchase_order__organization']
    search_fields = ['return_number', 'purchase_order__order_number']
    inlines = [PurchaseReturnItemInline]  # Adding inline items within PurchaseReturn admin page
    readonly_fields = ['return_number']  # Making return_number read-only as it is auto-generated

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('purchase_order')


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('bill_number', 'purchase', 'supplier', 'organization', 'total_amount', 'paid_amount', 'remaining_balance', 'status', 'issued_date', 'due_date')
    search_fields = ('bill_number', 'purchase__id', 'supplier__name')
    list_filter = ('status', 'issued_date', 'due_date')
    readonly_fields = ('created_at', 'updated_at')