from django.db import models
from django.conf import settings

class Organization(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    logo_image = models.ImageField(upload_to='organization_logos/', blank=True, null=True)
    address = models.ForeignKey("core.Address", on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class OrganizationUser(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="organizations"
    )
    organization = models.ForeignKey(
        "Organization",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="organization_users"
    )
    position = models.ForeignKey(
        "organization.Position",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="users"
    )
    role = models.ForeignKey(
        'user.UserRole',
        on_delete=models.CASCADE,
        related_name='users'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.organization}'


class OrganizationSetting(models.Model):
    COST_METHOD_CHOICES = [
        ('fifo', 'First In First Out (FIFO)'),
        ('average', 'Weighted Average Costing')
    ]

    organization = models.OneToOneField(Organization, on_delete=models.CASCADE, related_name='settings')
    cost_method = models.CharField(max_length=10, choices=COST_METHOD_CHOICES, default='fifo')

    def __str__(self):
        return f"Settings for {self.organization.name}"

class Position(models.Model):
    organization = models.ForeignKey(
        "Organization",
        on_delete=models.CASCADE,
        related_name="positions"
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Department(models.Model):
    organization = models.ForeignKey(
        "Organization",
        on_delete=models.CASCADE,
        related_name="departments"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name