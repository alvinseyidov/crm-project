from django.contrib import admin

from customer.models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'email', 'phone', 'industry', 'customer_type', 'lifetime_value', 'recent_purchase_date')
    list_filter = ('customer_type', 'industry', 'is_active', 'customer_since')
    search_fields = ('name', 'contact_person', 'email', 'phone', 'industry')
    ordering = ('name',)