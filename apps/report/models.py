from django.db import models
from django.utils.translation import ugettext_lazy as _

from helpers.model import BaseModel


class ActiveMonitoringSystemManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class MonitoringSystem(BaseModel):
    url = models.URLField(verbose_name=_('URL'), unique=True, help_text='URL of monitoring system')
    title = models.CharField(verbose_name=_('Title'), max_length=150, help_text='Title of monitoring system')
    start_page = models.IntegerField(verbose_name=_('Start'), default=0, help_text='First page of the URL')
    current_page = models.IntegerField(
        verbose_name=_('Current page'),
        default=0,
        help_text='Current page for pulling incident reports')
    last_status = models.IntegerField(null=True, blank=True, help_text="Status code of last request")
    last_update = models.DateTimeField(blank=True, null=True, help_text="Last time pull the incident reports")
    is_active = models.BooleanField(verbose_name=_('is active'), default=True)

    objects = models.Manager()
    active_objects = ActiveMonitoringSystemManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-create_time',)
        verbose_name = _('Monitoring system')
        verbose_name_plural = _('Monitoring systems')


class IncidentReport(BaseModel):
    class IncidentReportType(models.IntegerChoices):
        CUSTOM = 0, _('Custom, Admin created')
        PULL = 1, _('Pull, System pulled')

    incident = models.CharField(verbose_name=_('Incident'), max_length=250)
    position = models.IntegerField(verbose_name=_('Position'))
    monitoring_system = models.ForeignKey(
        to=MonitoringSystem,
        on_delete=models.CASCADE,
        related_name='reports',
        verbose_name=_('Monitoring system'),
        null=True)
    report_type = models.IntegerField(
        verbose_name=_('report type'),
        choices=IncidentReportType.choices,
        help_text="Admin created OR system pulled")

    def __str__(self):
        return self.incident

    class Meta:
        verbose_name = _('Incident report')
        verbose_name_plural = _('Incident reports')
