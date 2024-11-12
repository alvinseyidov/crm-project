from django.contrib import admin
from .models import Task, Effort

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'worker', 'customer', 'status', 'priority', 'deadline', 'organization')
    list_filter = ('status', 'priority', 'organization')
    search_fields = ('task_name', 'worker__name', 'customer__name', 'organization__name')
    ordering = ('deadline',)

@admin.register(Effort)
class EffortAdmin(admin.ModelAdmin):
    list_display = ('task', 'worker', 'date', 'hours_spent', 'organization')
    list_filter = ('date', 'organization')
    search_fields = ('task__task_name', 'worker__name', 'organization__name')
    ordering = ('date',)
