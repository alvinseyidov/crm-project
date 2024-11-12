from django.contrib import admin
from .models import *


class OrganizationSettingInline(admin.StackedInline):
    model = OrganizationSetting
    can_delete = False

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name','description','logo_image','address']
    inlines = [OrganizationSettingInline]



@admin.register(OrganizationUser)
class OrganizationUserAdmin(admin.ModelAdmin):
    list_display = ['user','organization','position','created_at','updated_at']


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['organization','name']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['organization','name','description']