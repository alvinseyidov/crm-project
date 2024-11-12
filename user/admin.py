from django.contrib import admin
from .models import *


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email','first_name','last_name']


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ['user','address','type']


@admin.register(UserPhone)
class UserPhoneAdmin(admin.ModelAdmin):
    list_display = ['user','phone','type']





@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ['organization','name','description','created_at','updated_at']


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['role','resource','create','update','view','delete']


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['name','description']