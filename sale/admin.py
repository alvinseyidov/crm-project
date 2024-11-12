from django.contrib import admin
from .models import SalesOrder, SalesOrderItem, SalesReturnOrderItem, SalesReturnOrder

# Admin for Customer


# Inline for SalesOrderItem
class SalesOrderItemInline(admin.TabularInline):
    model = SalesOrderItem
    extra = 1

# Admin for SalesOrder
@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'status', 'total_amount', 'tax_amount', 'grand_total', 'date', 'delivery_date')
    list_filter = ('status', 'date', 'delivery_date', 'created_at', 'updated_at')
    search_fields = ('order_number', 'customer__name')
    ordering = ('-date',)
    readonly_fields = ('total_amount', 'tax_amount', 'grand_total', 'created_at', 'updated_at')

    # Add SalesOrderItem inline
    inlines = [SalesOrderItemInline]




# Inline for ReturnOrderItem, to manage ReturnOrderItems within the ReturnOrder admin page
class SalesReturnOrderItemInline(admin.TabularInline):
    model = SalesReturnOrderItem
    extra = 1  # Number of empty slots for new items

# Admin for ReturnOrder
@admin.register(SalesReturnOrder)
class ReturnOrderAdmin(admin.ModelAdmin):
    list_display = ['return_number', 'sales_order', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'sales_order__organization']
    search_fields = ['return_number', 'sales_order__order_number']
    inlines = [SalesReturnOrderItemInline]  # Adding the inline items within ReturnOrder admin page
    readonly_fields = ['return_number']  # Making return_number read-only since it's auto-generated

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('sales_order')




