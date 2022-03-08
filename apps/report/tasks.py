import math
import threading

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import MonitoringSystem
from .services import MonitoringSystemService

User = get_user_model()


def pull_results(start, stop):
    for system in MonitoringSystem.active_objects.all()[start:stop]:
        monitoring_system_service = MonitoringSystemService(system)
        monitoring_system_service.pull_incident_report()


@shared_task
def pull_incident_report(*args, **kwargs):
    """
    Divide the urls into four parts and four thread, run faster
    """
    step = math.ceil(MonitoringSystem.active_objects.all().count() / 4)
    threads = list()
    for start in range(0, step * 3 + 1, step):
        pull_results(start, start + step)
        thread = threading.Thread(target=pull_results, args=(start, start + step))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return f'Pull incident reports at {timezone.now()}'
