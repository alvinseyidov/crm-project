from django.contrib import admin
from .models import *

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'address']  # Display these fields in the admin list view
    search_fields = ['name', 'organization__name']  # Add search functionality by warehouse name and organization name
    list_filter = ['organization']  # Add filtering by organization
    list_select_related = ['organization',]  # Optimize queries by using select_related for ForeignKey fields
    ordering = ['name']  # Set default ordering by warehouse name

    def get_queryset(self, request):
        # Override to use select_related for optimization
        queryset = super().get_queryset(request)
        return queryset.select_related('organization',)

    def __str__(self):
        return self.name  # Ensure a proper string representation in the admin site



from django.contrib import admin
from .models import Warehouse, Stock, StockBatch, StockMovement, StockAdjustment

# Inline for StockBatch to manage stock batches within the Warehouse admin page
class StockBatchInline(admin.TabularInline):
    model = StockBatch
    extra = 1
    readonly_fields = ['received_date']  # received_date is automatically generated

# Inline for Stock to manage stock levels within the Warehouse admin page
class StockInline(admin.TabularInline):
    model = Stock
    extra = 1
    readonly_fields = ['created_at', 'updated_at']


# Admin for Stock
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['product', 'warehouse', 'quantity', 'reserved_quantity', 'expected_quantity','available_stock',]
    search_fields = ['product__name', 'warehouse__name']
    list_filter = ['warehouse']
    readonly_fields = ['created_at', 'updated_at']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('product', 'warehouse')

# Admin for StockBatch
@admin.register(StockBatch)
class StockBatchAdmin(admin.ModelAdmin):
    list_display = ['product', 'warehouse', 'quantity', 'purchase_price', 'received_date']
    search_fields = ['product__name', 'warehouse__name']
    list_filter = ['warehouse', 'product']

# Admin for StockMovement
@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['product', 'warehouse', 'quantity', 'movement_type', 'movement_date', 'source_warehouse', 'destination_warehouse']
    search_fields = ['product__name', 'warehouse__name']
    list_filter = ['movement_type', 'warehouse']
    readonly_fields = ['movement_date']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('product', 'warehouse', 'source_warehouse', 'destination_warehouse')

# Admin for StockAdjustment
@admin.register(StockAdjustment)
class StockAdjustmentAdmin(admin.ModelAdmin):
    list_display = ['product', 'warehouse', 'quantity', 'adjustment_type', 'adjusted_at', 'reason']
    search_fields = ['product__name', 'warehouse__name']
    list_filter = ['adjustment_type', 'warehouse']
    readonly_fields = ['adjusted_at']
