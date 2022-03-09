from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import MonitoringSystem


@receiver(post_save, sender=MonitoringSystem)
def set_current_page_after_create(instance, created, *args, **kwargs):
    if created:
        instance.current_page = instance.start_page
        instance.save()
