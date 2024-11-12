from django.contrib import admin
from .models import Worker, Leave, Attendance

@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'organization', 'email', 'has_system_access', 'hours_worked', 'tasks_completed', 'employment_status')
    list_filter = ('organization', 'role', 'has_system_access', 'employment_status', 'date_joined')
    search_fields = ('name', 'email', 'role', 'organization__name')
    ordering = ('name',)

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('worker', 'organization', 'leave_type', 'start_date', 'end_date', 'approved')
    list_filter = ('organization', 'leave_type', 'approved', 'start_date', 'end_date')
    search_fields = ('worker__name', 'worker__email', 'organization__name')
    ordering = ('start_date',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('worker', 'organization', 'date', 'check_in_time', 'check_out_time', 'hours_worked')
    list_filter = ('organization', 'date', 'worker__role')
    search_fields = ('worker__name', 'worker__email', 'organization__name')
    ordering = ('date',)
