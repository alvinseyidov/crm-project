from django.contrib import admin
from .models import Expense, ExpenseCategory


@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'description')  # Fields to display in list view
    search_fields = ('name', 'organization__name')  # Fields to search
    list_filter = ('organization',)  # Filters by organization
    readonly_fields = ('created_at', 'updated_at')  # Fields to be read-only in detail view
    ordering = ('name',)  # Default ordering


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('category', 'organization', 'user', 'amount', 'status', 'date', 'created_at')  # Fields to display
    search_fields = ('category__name', 'user__username', 'organization__name', 'status')  # Fields to search
    list_filter = ('status', 'organization', 'category', 'date')  # Filters for the list view
    readonly_fields = ('submitted_at', 'approved_at', 'rejected_at', 'paid_at', 'created_at', 'updated_at')  # Fields to be read-only in detail view
    ordering = ('-date',)  # Default ordering by created date (most recent first)
    date_hierarchy = 'date'  # Adds a date hierarchy for filtering by date
