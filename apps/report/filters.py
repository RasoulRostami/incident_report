import django_filters

from .models import IncidentReport


class IncidentReportFiler(django_filters.FilterSet):
    create_time_gte = django_filters.DateTimeFilter(field_name='create_time', lookup_expr='gte')
    create_time_lte = django_filters.DateTimeFilter(field_name='create_time', lookup_expr='lte')
    modify_time_gte = django_filters.DateTimeFilter(field_name='modify_time', lookup_expr='gte')
    modify_time_lte = django_filters.DateTimeFilter(field_name='modify_time', lookup_expr='lte')

    class Meta:
        model = IncidentReport
        fields = (
            'create_time_gte',
            'create_time_lte',
            'modify_time_gte',
            'modify_time_lte',
            'monitoring_system_id',
            'report_type')