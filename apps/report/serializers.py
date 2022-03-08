from django.utils.translation import ugettext as _
from rest_framework import serializers

from .models import MonitoringSystem, IncidentReport


class MonitoringSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringSystem
        fields = ('id', 'title')


class IncidentReportSerializer(serializers.ModelSerializer):
    monitoring_system = MonitoringSystemSerializer(read_only=True)
    monitoring_system_id = serializers.PrimaryKeyRelatedField(
        queryset=MonitoringSystem.active_objects.all(), write_only=True, allow_null=True)
    translated_report_type = serializers.CharField(source='get_report_type_display', read_only=True)

    class Meta:
        model = IncidentReport
        fields = (
            'id',
            'monitoring_system',
            'monitoring_system_id',
            'incident',
            'position',
            'report_type',
            'translated_report_type')

    def validate_report_type(self, value):
        if value != IncidentReport.IncidentReportType.CUSTOM:
            raise serializers.ValidationError(_('You are not able to create pull type'))
        return value
