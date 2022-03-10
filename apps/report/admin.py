from django.contrib.admin import register

from helpers.admin import BaseAdminModel
from .models import MonitoringSystem, IncidentReport


@register(MonitoringSystem)
class MonitoringSystemAdmin(BaseAdminModel):
    readonly_fields = ('current_page', 'last_status', 'last_update')
    fieldsets = (
        (None, {"fields": ['title', 'url', 'start_page', 'is_active']}),
        ('Logs Data', {"fields": ['current_page', 'last_status', 'last_update']})
    )
    list_filter = ('is_active',)


@register(IncidentReport)
class IncidentReportAdmin(BaseAdminModel):
    list_display = ('id', 'monitoring_system', 'position', 'incident')
    list_filter = ('report_type',)
