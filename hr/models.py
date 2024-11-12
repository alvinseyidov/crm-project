from datetime import datetime, date

from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Worker(models.Model):
    ROLE_CHOICES = [
        ('HR', 'Human Resources'),
        ('AC', 'Accountant'),
        ('MG', 'Manager'),
        ('SP', 'Sales Person'),
        ('OT', 'Other'),
    ]
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE)  # Link to the organization
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    # This field allows linking to a User object for workers with system access.
    # It's nullable for workers who don't need system access.

    name = models.CharField(max_length=255)
    role = models.CharField(max_length=2, choices=ROLE_CHOICES)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    date_joined = models.DateField(auto_now_add=True)
    hours_worked = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    tasks_completed = models.IntegerField(default=0)

    # Payroll-related fields for workers who don’t need system access
    payroll = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    employment_status = models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')

    # Fields to differentiate workers with or without system access
    has_system_access = models.BooleanField(default=False)  # Tracks whether the worker can log in and access the system.

    def __str__(self):
        return f'{self.name} - {self.get_role_display()}'

    def get_access_level(self):
        if self.has_system_access:
            return "Has system access"
        return "Record-only (no access)"



class Attendance(models.Model):
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE)  # Link to the organization
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    date = models.DateField()
    check_in_time = models.TimeField()
    check_out_time = models.TimeField(null=True, blank=True)
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def calculate_hours_worked(self):
        if self.check_in_time and self.check_out_time:
            # Calculate the difference between check-in and check-out times
            time_diff = datetime.combine(date.min, self.check_out_time) - datetime.combine(date.min, self.check_in_time)
            self.hours_worked = time_diff.total_seconds() / 3600  # Convert seconds to hours
        return self.hours_worked

    def __str__(self):
        return f'Attendance for {self.worker.name} on {self.date}'


class Leave(models.Model):
    LEAVE_TYPES = [
        ('ANNUAL', 'Annual Leave'),
        ('SICK', 'Sick Leave'),
        ('UNPAID', 'Unpaid Leave'),
        ('MATERNITY', 'Maternity Leave'),
    ]
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE)  # Link to the organization
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=10, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.worker.name} - {self.get_leave_type_display()} from {self.start_date} to {self.end_date}'


