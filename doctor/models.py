from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Zone(models.Model):
    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=256)
    group = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}'


class Branch(models.Model):
    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=256)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Hospital(models.Model):
    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE,
        related_name="hospitals"
    )
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name="hospitals")
    name = models.CharField(max_length=256)
    address = models.CharField(max_length=256, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('zone', 'name',)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    CATEGORY = (
        ('A**', 'PLATINIUM'),
        ('A*', 'VIP'),
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('I', 'I'),
    )
    GENDER = (
        ('K', 'Kişi'),
        ('Q', 'Qadın'),
    )
    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE,
        related_name="doctors"
    )
    code = models.CharField(max_length=256, null=True, blank=True, unique=True)
    category = models.CharField(max_length=5, default='A', choices=CATEGORY)
    full_name = models.CharField(max_length=256)
    email = models.CharField(max_length=256, null=True, blank=True)
    phone = models.CharField(max_length=256, null=True, blank=True)
    percent = models.IntegerField(default=0)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="doctors", null=True, blank=True)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name="doctors")
    city = models.ForeignKey("core.City", on_delete=models.CASCADE, null=True, blank=True, related_name="doctors")
    hospital = models.ForeignKey(Hospital, null=True, blank=True, on_delete=models.CASCADE, related_name="doctors")
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    gender = models.CharField(max_length=1, default='K', choices=GENDER)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('hospital', 'full_name',)

    def __str__(self):
        return f'{self.full_name} - {self.percent}% - {self.zone.name}'
