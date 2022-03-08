import json

import requests
from django.utils import timezone
from rest_framework import status

from .models import MonitoringSystem, IncidentReport


class MonitoringSystemService:
    def __init__(self, system: MonitoringSystem):
        self.system = system

    def pull_incident_report(self):
        response = requests.get(self._current_url())
        if response.status_code != status.HTTP_200_OK:
            self._update_request_data(response.status_code)
        else:
            self._save_new_incident_report(json.loads(response.content))
            self._update_request_data(response.status_code, self.system.current_page + 1)

    def _current_url(self):
        return f"{self.system.url}?start={self.system.current_page}"

    def _update_request_data(self, status_code: int, next_page: int = None):
        """ Update request data of monitoring system after new request """
        if next_page:
            self.system.current_page = next_page

        self.system.last_status = status_code
        self.system.last_update = timezone.now()
        self.system.save()

    def _save_new_incident_report(self, results: list):
        incident_reports = list()
        for report in results:
            incident_reports.append(
                IncidentReport(monitoring_system_id=self.system.id,
                               incident=report['incident'],
                               position=report['position'],
                               report_type=IncidentReport.IncidentReportType.PULL)
            )
        IncidentReport.objects.bulk_create(incident_reports)
