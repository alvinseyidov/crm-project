from django.contrib import admin
from .models import Zone, Branch, Hospital, Doctor


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'group', 'is_active')
    list_filter = ('organization', 'is_active', 'group')
    search_fields = ('name',)


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization')
    list_filter = ('organization',)
    search_fields = ('name',)


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'zone', 'organization', 'address', 'created_at', 'updated_at')
    list_filter = ('organization', 'zone')
    search_fields = ('name', 'address')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'category', 'branch', 'zone', 'hospital', 'percent', 'gender', 'is_active', 'created_at')
    list_filter = ('organization','category', 'gender', 'is_active', 'branch', 'zone', 'hospital')
    search_fields = ('full_name', 'email', 'phone', 'code')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('code', 'full_name', 'email', 'phone', 'percent', 'category', 'gender', 'is_active', 'description', 'image')
        }),
        ('Organization Details', {
            'fields': ('organization','branch', 'zone', 'city', 'hospital')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
