from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import MonitoringSystem


@receiver(post_save, sender=MonitoringSystem)
def change_order_status(instance, created, *args, **kwargs):
    if created:
        instance.current_page = instance.start_page
        instance.save()
