from django.db import models
from django.contrib.auth.models import AbstractUser
from user.managers import CustomUserManager


class CustomUser(AbstractUser):
    GENDER = (
        ('K', 'Kişi'),
        ('Q', 'Qadın'),
        ('D', 'Digər')
    )
    username = None
    email = models.EmailField(max_length=128, unique=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    date_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER, blank=True, null=True)
    position =  models.ForeignKey(
        'organization.Position',
        on_delete=models.PROTECT, 
        related_name='positions',
        null=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.last_name} {self.first_name}'
    

class UserAddress(models.Model):
    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='addresses'
    )
    address = models.ForeignKey(
        'core.Address', 
        on_delete=models.CASCADE
    )
    type = models.CharField(max_length=255)

class UserPhone(models.Model):
    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='phones'
    )
    phone = models.ForeignKey(
        "core.Phone",
        on_delete=models.CASCADE,
        related_name='user'
    )
    type = models.CharField(max_length=255)



class UserRole(models.Model):
    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE,
        related_name='user_roles'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Permission(models.Model):
    role = models.ForeignKey(
        UserRole, 
        on_delete=models.CASCADE, 
        related_name='permissions'
    )
    resource = models.ForeignKey(
        'Resource', 
        on_delete=models.CASCADE
    ) 
    create = models.BooleanField(default=False)
    update = models.BooleanField(default=False)
    view = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.role.name} - {self.resource.name}'

class Resource(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class ModuleAccess(models.Model):
    organization = models.ForeignKey(
        "organization.Organization",
        on_delete=models.CASCADE,
        related_name='module_accesses'
    )
    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        related_name='module_accesses'
    )
    has_access = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.organization.name} - {self.resource.name} - {self.has_access}'