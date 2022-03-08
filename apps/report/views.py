from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import GenericViewSet

from .filters import IncidentReportFiler
from .models import IncidentReport
from .serializers import IncidentReportSerializer


class IncidentReportView(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = IncidentReport.objects.all().select_related('monitoring_system')
    serializer_class = IncidentReportSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IncidentReportFiler

    def get_permissions(self):
        if self.action == 'create':
            return [IsAdminUser]
        return [IsAuthenticated]
