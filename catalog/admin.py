from django.contrib import admin
from django.db import models
from django.db import IntegrityError
from django.utils.html import format_html

from inventory.models import Stock  # Import the Stock model

from .models import (
    Category, Brand, ProductAttribute, ProductAttributeValue,
    Product, ProductImage, ProductCost, ProductPrice, Manufacturer, ProductCostHistory
)
from django.core.exceptions import ValidationError

# Inline for ProductAttributeValue inside ProductAttribute
class ProductAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue
    extra = 1
    fields = ('value',)
    min_num = 1
    verbose_name = "Attribute Value"
    verbose_name_plural = "Attribute Values"

# Admin for ProductAttribute
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization')
    list_filter = ('organization',)
    search_fields = ('name', 'organization__name')
    ordering = ('name',)
    inlines = [ProductAttributeValueInline]

# Admin for ProductAttributeValue
class ProductAttributeValueAdmin(admin.ModelAdmin):
    list_display = ('attribute', 'value', 'organization')
    list_filter = ('attribute__organization', 'attribute')
    search_fields = ('attribute__name', 'value', 'attribute__organization__name')

    def save_model(self, request, obj, form, change):
        # Automatically assign the organization if it's not set
        if not obj.organization:
            obj.organization = obj.attribute.organization  # Inherit from the related attribute
        super().save_model(request, obj, form, change)

# Admin for Brand
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'created_at', 'updated_at')
    search_fields = ('name', 'organization__name')
    list_filter = ('organization',)
    readonly_fields = ('logo_image', 'created_at', 'updated_at')

    def logo_image(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.logo.url)
        return "No Image"

    logo_image.short_description = 'Logo'

    fieldsets = (
        (None, {
            'fields': ('organization', 'name', 'description', 'logo', 'logo_image')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization')
    list_filter = ('organization',)
    search_fields = ('name', 'organization__name')
    ordering = ('name',)



# Inline for ProductImage inside Product
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'sorting')
    ordering = ('sorting',)

# Inline for ProductPrice inside Product
class ProductPriceInline(admin.TabularInline):
    model = ProductPrice
    extra = 1
    fields = ('amount', 'date')
    ordering = ('-date',)

# Inline for ProductCost inside Product
class ProductCostInline(admin.TabularInline):
    model = ProductCost
    extra = 1
    fields = ('amount', 'date', 'vendor')
    ordering = ('-date',)

# Admin for Product
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'barcode', 'category', 'type', 'organization', 'is_active', 'price', 'total_stock')  # Add 'total_stock'
    list_filter = ('organization', 'type', 'brand', 'is_active')
    search_fields = ('name', 'sku', 'barcode', 'brand__name', 'organization__name')
    ordering = ('name',)
    list_per_page = 20

    # Inline management of product images, prices, and costs
    inlines = [ProductImageInline, ProductPriceInline, ProductCostInline]

    # Organize the product detail page in fieldsets
    fieldsets = (
        (None, {
            'fields': ('organization', 'name', 'sku', 'barcode', 'category', 'description', 'type', 'measurement', 'tax', 'brand','manufacturer')
        }),
        ('Attributes', {
            'fields': ('attributes',),
        }),
        ('Status', {
            'fields': ('is_active', 'is_deleted')
        }),
        ('Meta Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),  # Collapse this section
        }),
    )

    # Readonly fields for timestamps
    readonly_fields = ('created_at', 'updated_at')

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super(ProductAdmin, self).get_inline_instances(request, obj)

    def save_model(self, request, obj, form, change):
        try:
            obj.save()
        except ValueError as e:
            form.add_error(None, ValidationError(str(e)))
        except IntegrityError as e:
            form.add_error(None, ValidationError("A product with the same name already exists in this organization."))

    def total_stock(self, obj):
        """Return the total stock for the product across all warehouses."""
        stock = Stock.objects.filter(product=obj).aggregate(total=models.Sum('quantity'))['total']
        return stock or 0  # Return 0 if no stock exists
    total_stock.short_description = 'Total Stock'  # Column header in the admin list



class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'parent', 'is_active', 'created_at', 'updated_at')
    list_filter = ('organization', 'is_active')
    search_fields = ('name', 'organization__name')
    readonly_fields = ('created_at', 'updated_at')
    fields = ('organization', 'parent', 'name', 'description', 'image', 'is_active', 'created_at', 'updated_at')

    def get_queryset(self, request):
        """
        Custom queryset to order categories in a way that reflects the hierarchy.
        """
        qs = super().get_queryset(request)
        return qs.order_by('parent__id', 'name')  # Sorts by parent first, then by name

    def display_hierarchy(self, obj):
        """
        Display the hierarchical structure with indentation.
        """
        level = 0
        current = obj
        while current.parent is not None:
            level += 1
            current = current.parent
        indent = "-- " * level
        return f"{indent}{obj.name}"

    display_hierarchy.short_description = 'Category Name'

    list_display = ('display_hierarchy', 'organization', 'is_active', 'created_at', 'updated_at')


admin.site.register(Category, CategoryAdmin)

admin.site.register(Brand, BrandAdmin)
admin.site.register(ProductAttribute, ProductAttributeAdmin)
admin.site.register(ProductAttributeValue, ProductAttributeValueAdmin)
admin.site.register(Product, ProductAdmin)

@admin.register(ProductCostHistory)
class ProductCostHistoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'purchase', 'cost_date', 'unit_cost', 'landed_cost', 'total_cost')
    list_filter = ('product', 'cost_date')
    search_fields = ('product__name', 'purchase__order_number')
    readonly_fields = ('cost_date', 'total_cost')
    date_hierarchy = 'cost_date'

    def save_model(self, request, obj, form, change):
        # Ensure total_cost is recalculated when saving from admin
        obj.total_cost = obj.unit_cost + obj.landed_cost
        super().save_model(request, obj, form, change)

