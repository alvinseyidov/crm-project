from django.db import models
from hr.models import Worker


class Task(models.Model):
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE)  # Link to the organization
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)  # Worker assigned to the task
    customer = models.ForeignKey('customer.Customer', on_delete=models.SET_NULL, blank=True,
                                 null=True)  # Optional customer link

    task_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('in_progress', 'In Progress'),
                                                      ('completed', 'Completed')], default='pending')
    priority = models.CharField(max_length=50, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
                                default='medium')

    deadline = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task_name


class Effort(models.Model):
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE)  # Link to the organization
    task = models.ForeignKey(Task, on_delete=models.CASCADE)  # Link to the task
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)  # The worker logging the effort

    date = models.DateField()  # Date when the work was done
    hours_spent = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)  # Number of hours worked on that day
    notes = models.TextField(blank=True, null=True)  # Optional field to add notes about the effort (e.g., work done)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Effort by {self.worker.name} on {self.date} for {self.task.task_name}'