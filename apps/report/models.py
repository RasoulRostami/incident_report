from django.db import models
from django.utils.translation import ugettext_lazy as _

from helpers.model import BaseModel


class ActiveRSSFeedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class MonitoringSystem(BaseModel):
    url = models.URLField(verbose_name=_('URL'), unique=True, help_text='URL of monitoring system')
    title = models.CharField(verbose_name=_('Title'), max_length=150, help_text='Title of monitoring system')
    start_page = models.IntegerField(verbose_name=_('Start'), default=0, help_text='First page of the URL')
    last_status = models.IntegerField(null=True, blank=True, help_text="Status code of last request", editable=False)
    last_update = models.DateTimeField(blank=True, null=True, help_text="Last time pull the incident reports", editable=False)
    is_active = models.BooleanField(
        default=True, help_text="A monitoring system will become inactive when a permanent error occurs", editable=False)

    objects = models.Manager()
    active_objects = ActiveRSSFeedManager()

    class Meta:
        verbose_name = _('Monitoring system')
        verbose_name_plural = _('Monitoring systems')


class IncidentReport(BaseModel):
    class IncidentReportType(models.IntegerChoices):
        CUSTOM = 0, _('Custom, Admin created')
        PULL = 1, _('Pull, System pulled')

    monitoring_system = models.ForeignKey(
        to=MonitoringSystem,
        on_delete=models.CASCADE,
        related_name='reports',
        verbose_name=_('Monitoring system'),
        null=True)
    incident = models.CharField(verbose_name=_('Incident'), max_length=250)
    position = models.IntegerField(verbose_name=_('Position'))
    report_type = models.IntegerField(verbose_name=_('report type'), help_text="Admin created OR system pulled")

    class Meta:
        verbose_name = _('Incident report')
        verbose_name_plural = _('Incident reports')
