from django.contrib.admin import register

from helpers.admin import BaseAdminModel
from .models import MonitoringSystem, IncidentReport


@register(MonitoringSystem)
class MonitoringSystemAdmin(BaseAdminModel):
    list_display = ('title', 'url', 'start_page', 'last_update', 'last_status')
    list_filter = ('is_active',)


@register(IncidentReport)
class IncidentReportAdmin(BaseAdminModel):
    list_display = ('id', 'monitoring_system', 'position', 'incident')
    list_filter = ('report_type',)
