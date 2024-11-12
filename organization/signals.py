from django.db.models.signals import post_save
from django.dispatch import receiver

from organization.models import Organization, OrganizationSetting


@receiver(post_save, sender=Organization)
def create_organization_setting(sender, instance, created, **kwargs):
    if created:
        OrganizationSetting.objects.create(organization=instance)